#!/bin/bash

# ============================================
# Cloud NMS 部署脚本
# ============================================

set -e  # 遇到错误立即退出

# ============================================
# 配置参数
# ============================================

SERVER_IP="192.168.0.98"
SERVER_USER="cloud_nms"
SERVER_PASSWORD="Genew1234"
DB_PASSWORD="1Z_kF8s2mHcTnQHC"
LOCAL_BUILD_PATH="/Users/farghost/IdeaProjects/HuahaiPlatform2/output"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ============================================
# 工具函数
# ============================================

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

confirm() {
    read -p "$(echo -e ${YELLOW}$1${NC}) (y/n): " -n 1 -r
    echo
    [[ $REPLY =~ ^[Yy]$ ]]
}

ssh_exec() {
    sshpass -p "$SERVER_PASSWORD" ssh -o StrictHostKeyChecking=no "$SERVER_USER@$SERVER_IP" "$1"
}

# ============================================
# 主要功能函数
# ============================================

check_dependencies() {
    log_info "检查依赖工具..."
    if ! command -v sshpass &> /dev/null; then
        log_error "未找到 sshpass 工具，请先安装: brew install sshpass"
        exit 1
    fi
    log_success "依赖检查通过"
}

uninstall_services() {
    log_warning "即将卸载所有 Cloud NMS 服务"
    if ! confirm "确认要卸载吗？此操作会删除所有数据！"; then
        log_info "已取消卸载操作"
        return 1
    fi

    log_info "卸载现有服务..."
    
    ssh_exec "cd /usr/local/cloud_nms/service/ && ./uninstall_all.sh" || log_warning "uninstall_all.sh 执行失败或服务不存在"
    
    ssh_exec "
        cd ~ && \
        rm -rf CloudNMSDummyBusiness_* && \
        rm -rf CloudNMSPlatform_* && \
        sudo rm -rf /usr/local/cloud_nms/env/nginx/html/platform && \
        sudo rm -rf /usr/local/cloud_nms/env/nginx/html/ems
    "
    
    log_success "卸载完成"
    
    # 验证
    log_info "验证卸载结果..."
    ssh_exec "ls -la /usr/local/cloud_nms/service/ 2>/dev/null || echo '服务目录已清空'"
}

upload_packages() {
    local version=$1
    
    log_info "上传安装包 (版本: $version)..."
    
    # 检查本地文件是否存在
    if [[ ! -f "$LOCAL_BUILD_PATH/CloudNMSPlatform_$version.zip" ]]; then
        log_error "平台安装包不存在: $LOCAL_BUILD_PATH/CloudNMSPlatform_$version.zip"
        return 1
    fi
    
    if [[ ! -f "$LOCAL_BUILD_PATH/CloudNMSDummyBusiness_$version.zip" ]]; then
        log_error "业务安装包不存在: $LOCAL_BUILD_PATH/CloudNMSDummyBusiness_$version.zip"
        return 1
    fi
    
    log_info "上传 CloudNMSPlatform_$version.zip..."
    sshpass -p "$SERVER_PASSWORD" scp -o StrictHostKeyChecking=no \
        "$LOCAL_BUILD_PATH/CloudNMSPlatform_$version.zip" \
        "$SERVER_USER@$SERVER_IP:~/"
    
    log_info "上传 CloudNMSDummyBusiness_$version.zip..."
    sshpass -p "$SERVER_PASSWORD" scp -o StrictHostKeyChecking=no \
        "$LOCAL_BUILD_PATH/CloudNMSDummyBusiness_$version.zip" \
        "$SERVER_USER@$SERVER_IP:~/"
    
    log_success "上传完成"
    
    # 验证
    log_info "验证上传文件..."
    ssh_exec "ls -lh ~/*.zip"
}

install_fresh() {
    local version=$1
    
    log_info "执行全新安装 (版本: $version)..."
    
    ssh_exec "
        cd ~ && \
        unzip -o CloudNMSPlatform_$version.zip && \
        chmod -R 755 CloudNMSPlatform_$version && \
        cd CloudNMSPlatform_$version && \
        sed -i 's|127.0.0.1|$SERVER_IP|' set_env.sh && \
        sed -i 's|language=zh|language=en|' set_env.sh && \
        sed -i 's|country=CN|country=US|' set_env.sh && \
        ./install_platform.sh && \
        cd .. && \
        cp license.xml.sig /usr/local/cloud_nms/service/base-service
    "
    
    log_success "平台服务安装完成"
    
    ssh_exec "
        cd ~ && \
        unzip -o CloudNMSDummyBusiness_$version.zip && \
        chmod -R 755 CloudNMSDummyBusiness_$version && \
        cd CloudNMSDummyBusiness_$version && \
        sed -i 's|127.0.0.1|$SERVER_IP|' set_env.sh && \
        sed -i 's|language=zh|language=en|' set_env.sh && \
        sed -i 's|country=CN|country=US|' set_env.sh && \
        ./install_dummy_business.sh && \
        ./start_all.sh
    "
    
    log_success "业务服务安装完成"
    
    log_info "等待服务启动 (5秒)..."
    sleep 5
    
    log_info "初始化数据库用户..."
    init_database
    
    log_success "全新安装完成！"
}

install_lite() {
    local version=$1
    
    log_info "执行保留数据安装 (版本: $version)..."
    
    ssh_exec "
        cd ~ && \
        unzip -o CloudNMSPlatform_$version.zip && \
        chmod -R 755 CloudNMSPlatform_$version && \
        cd CloudNMSPlatform_$version && \
        sed -i 's|127.0.0.1|$SERVER_IP|' set_env.sh && \
        sed -i 's|language=zh|language=en|' set_env.sh && \
        sed -i 's|country=CN|country=US|' set_env.sh && \
        ./install_platform_lite.sh && \
        cd .. && \
        cp license.xml.sig /usr/local/cloud_nms/service/base-service
    "
    
    log_success "平台服务升级完成"
    
    ssh_exec "
        cd ~ && \
        unzip -o CloudNMSDummyBusiness_$version.zip && \
        chmod -R 755 CloudNMSDummyBusiness_$version && \
        cd CloudNMSDummyBusiness_$version && \
        sed -i 's|127.0.0.1|$SERVER_IP|' set_env.sh && \
        sed -i 's|language=zh|language=en|' set_env.sh && \
        sed -i 's|country=CN|country=US|' set_env.sh && \
        ./install_dummy_business_lite.sh && \
        ./start_all.sh
    "
    
    log_success "业务服务升级完成"
    
    log_info "等待服务启动 (5秒)..."
    sleep 5
    
    log_success "保留数据安装完成！"
}

init_database() {
    log_info "初始化数据库用户..."
    
    # 创建临时 SQL 文件
    local sql_file="/tmp/init_cloudnms_users.sql"
    
    cat > "$sql_file" << 'EOF'
UPDATE nmsuser 
SET ifFirstLogin = false, 
    password = '54954cf34d9a328f6a9e650e300e610593aae5539146b9c35f0cc1b69e0d3103cf8ff36377c2d5943853748821ee80b62875cc14363ebf1a951afaee67ec9cb9', 
    passwordSalt = 'ili9gn0jtjhh16sh' 
WHERE id = 1;

INSERT INTO nmsuser (id, version, beEffective, createDate, creator, flag, ifSm, isLocked, loginFailNumber, password, passwordSalt, passwordModifyDate, passwordValidDays, reserved, userGroup_id, userName, ifSecondaryAuthConfirm, ifFirstLogin, timeZone, dateFormat, timeFormat, showModel, timeAndIpControlStrategy) 
VALUES
(2, 0, true, CURRENT_DATE, 'admin', '0:-1', false, false, 0, '1f5c449574a7120e801a4f281231b9fdae45da206d5647a52eadf835e18fd642c185330baa4bc667d95e4393a3d50d61b7b6c7b49457618076d2bdf48d6290cb', '6zfssrman3p41hsn', CURRENT_DATE, 180, false, -1, 'caowentao', false, false, 'default', 'yyyy-MM-dd', 'HH:mm:ss', 0, -1),
(5, 0, true, CURRENT_DATE, 'admin', '0:-1', false, false, 0, '271804146b3c455ad2e2aa98a4ffc2d3b9b58cdc039f2d85e79f5d9f5eda66b84f61d55c808fc1e5c7a2b23198ea13b6c4c4acfaa627b4e257aca440c56a2a62', 'gupwnjqmm6ghgorf', CURRENT_DATE, 180, false, -1, 'liucheng', false, false, 'default', 'yyyy-MM-dd', 'HH:mm:ss', 0, -1),
(7, 0, true, CURRENT_DATE, 'admin', '0:-1', false, false, 0, 'cc01072558f1be48ab633e658117d02b069629fd0a65c5d2af5fbce769da879c6f693cc18f2ce97351f68a0f6fd0bcdcb8ecd31b846828b6b506963c244d63f0', '3weymxz5shyky6qk', CURRENT_DATE, 180, false, -1, 'yangxinyuan', false, false, 'default', 'yyyy-MM-dd', 'HH:mm:ss', 0, -1),
(8, 0, true, CURRENT_DATE, 'admin', '0:-1', false, false, 0, '6590288491805cf8ed2d2a44c94da2ceb5b541335bae554bb8893ece3bb17de42437fc712ba3839c7478cb805d5d9a9e9980c2bd18ff210bb2bef4806c6fb139', '086v88cip971wm4b', CURRENT_DATE, 180, false, -1, 'qiyongfeng', false, false, 'default', 'yyyy-MM-dd', 'HH:mm:ss', 0, -1),
(9, 0, true, CURRENT_DATE, 'admin', '0:-1', false, false, 0, 'd5f345984c72c0ab9d896633bc172005f3134529e151156be5a423abfe5540df1e0ab5c31ad1864e35525184f33174219bd09c14ddf8f8996274d286c00fb4d4', 'cgiurnoy1pa0iar9', CURRENT_DATE, 180, false, -1, 'guohuihua', false, false, 'default', 'yyyy-MM-dd', 'HH:mm:ss', 0, -1),
(10, 0, true, CURRENT_DATE, 'admin', '0:-1', false, false, 0, '4086ec9c5a621c5ef67504ccd98ef997e48e2c988b8d031879347f7516ca6741835d5c9b30f81b36918b43a09810f98d0f06721c5d5ee400cc19999eb59aeb3e', 'dqxjy2fd8ag04vl3', CURRENT_DATE, 180, false, -1, 'panming', false, false, 'default', 'yyyy-MM-dd', 'HH:mm:ss', 0, -1)
ON DUPLICATE KEY UPDATE id=id;
EOF
    
    ssh_exec "mysql -u cloud_nms -p'$DB_PASSWORD' cloud_nms < /dev/stdin" < "$sql_file" 2>/dev/null || {
        log_warning "数据库初始化失败，请手动执行 SQL"
        log_info "SQL 文件位置: $sql_file"
        return 1
    }
    
    rm -f "$sql_file"
    log_success "数据库初始化完成"
}

verify_deployment() {
    log_info "验证部署状态..."
    
    echo ""
    log_info "=== 服务进程状态 ==="
    ssh_exec "ps aux | grep cloud_nms | grep -v grep" || log_warning "未找到运行中的服务进程"
    
    echo ""
    log_info "=== 最近 20 行日志 ==="
    ssh_exec "tail -n 20 ~/logs/service/base-service.log 2>/dev/null" || log_warning "无法读取日志文件"
    
    echo ""
    log_success "访问地址: http://$SERVER_IP/platform"
    log_info "默认账户: admin / 默认密码"
}

view_logs() {
    log_info "查看实时日志 (按 Ctrl+C 退出)..."
    ssh_exec "tail -f ~/logs/service/base-service.log"
}

# ============================================
# 主菜单
# ============================================

show_menu() {
    echo ""
    echo -e "${BLUE}======================================${NC}"
    echo -e "${BLUE}  Cloud NMS 部署管理脚本${NC}"
    echo -e "${BLUE}======================================${NC}"
    echo "  服务器: $SERVER_USER@$SERVER_IP"
    echo "  构建路径: $LOCAL_BUILD_PATH"
    echo -e "${BLUE}======================================${NC}"
    echo "  1) 卸载现有版本"
    echo "  2) 上传安装包"
    echo "  3) 全新安装 (清空数据)"
    echo "  4) 保留数据安装 (升级)"
    echo "  5) 验证部署状态"
    echo "  6) 查看实时日志"
    echo "  0) 退出"
    echo -e "${BLUE}======================================${NC}"
}

show_usage() {
    cat << EOF
使用方法:
  交互式模式:
    $0

  命令行模式:
    $0 <version> <mode>

参数说明:
  version    版本号，例如: 1.1.0.6
  mode       安装模式:
              - fresh: 全新安装（清空数据）
              - lite: 保留数据安装（升级）

示例:
  $0 1.1.0.6 fresh         # 全新安装 1.1.0.6
  $0 1.1.0.6 lite          # 保留数据安装 1.1.0.6

EOF
}

interactive_mode() {
    while true; do
        show_menu
        read -p "请选择操作 [0-6]: " choice
        
        case $choice in
            1)
                uninstall_services
                ;;
            2)
                read -p "请输入版本号 (例如 1.1.0.6): " version
                while [[ -z "$version" ]]; do
                    log_error "版本号不能为空！"
                    read -p "请输入版本号: " version
                done
                upload_packages "$version"
                ;;
            3)
                read -p "请输入版本号 (例如 1.1.0.6): " version
                while [[ -z "$version" ]]; do
                    log_error "版本号不能为空！"
                    read -p "请输入版本号: " version
                done
                install_fresh "$version"
                verify_deployment
                ;;
            4)
                read -p "请输入版本号 (例如 1.1.0.6): " version
                while [[ -z "$version" ]]; do
                    log_error "版本号不能为空！"
                    read -p "请输入版本号: " version
                done
                install_lite "$version"
                verify_deployment
                ;;
            5)
                verify_deployment
                ;;
            6)
                view_logs
                ;;
            0)
                log_info "退出脚本"
                exit 0
                ;;
            *)
                log_error "无效选择，请重新输入"
                ;;
        esac
        
        echo ""
        read -p "按 Enter 键继续..."
    done
}

command_mode() {
    local version=$1
    local mode=$2
    
    # 验证版本号
    if [[ -z "$version" ]]; then
        log_error "错误：版本号不能为空"
        show_usage
        exit 1
    fi
    
    # 验证模式
    if [[ -z "$mode" ]]; then
        log_error "错误：安装模式不能为空"
        show_usage
        exit 1
    fi
    
    case $mode in
        fresh)
            log_info "命令行模式: 全新安装 $version"
            upload_packages "$version"
            install_fresh "$version"
            verify_deployment
            ;;
        lite)
            log_info "命令行模式: 保留数据安装 $version"
            upload_packages "$version"
            install_lite "$version"
            verify_deployment
            ;;
        *)
            log_error "错误：无效的安装模式 '$mode'"
            log_info "有效模式: fresh, lite"
            show_usage
            exit 1
            ;;
    esac
}

main() {
    check_dependencies
    
    # 判断是命令行模式还是交互式模式
    if [[ $# -eq 0 ]]; then
        # 无参数，进入交互式模式
        interactive_mode
    elif [[ $1 == "-h" ]] || [[ $1 == "--help" ]]; then
        show_usage
        exit 0
    else
        # 有参数，使用命令行模式
        command_mode "$1" "$2"
    fi
}

# ============================================
# 脚本入口
# ============================================

main "$@"
