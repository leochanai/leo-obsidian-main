#!/bin/bash

# ============================================
# Cloud NMS 部署 - 步骤 3: 安装服务
# ============================================
# 用法: ./03_install.sh <version> <mode>
# 示例: ./03_install.sh 1.1.0.6 fresh
# ============================================

set -e

# 加载公共配置
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"

# ============================================
# 校验函数
# ============================================

verify_before_install() {
    local version=$1
    
    log_info "检查安装前状态..."
    
    # 检查安装包是否存在
    if ! ssh_exec "test -f ~/CloudNMSPlatform_$version.zip" &>/dev/null; then
        log_error "❌ 安装包不存在: ~/CloudNMSPlatform_$version.zip"
        log_info "请先运行: ./02_upload.sh $version"
        return 1
    fi
    log_success "✅ 平台安装包存在"
    
    if ! ssh_exec "test -f ~/CloudNMSDummyBusiness_$version.zip" &>/dev/null; then
        log_error "❌ 安装包不存在: ~/CloudNMSDummyBusiness_$version.zip"
        log_info "请先运行: ./02_upload.sh $version"
        return 1
    fi
    log_success "✅ 业务安装包存在"
    
    # 检查服务目录是否已存在（可能需要先卸载）
    if ssh_exec "test -d /usr/local/cloud_nms/service && ls /usr/local/cloud_nms/service/*.jar" &>/dev/null 2>&1; then
        log_warning "⚠️ 检测到已安装的服务"
        ssh_exec "ls /usr/local/cloud_nms/service/*.jar | head -5" 2>/dev/null || true
        if ! confirm "是否继续安装（将覆盖现有服务）？"; then
            log_info "已取消，请先运行 ./01_uninstall.sh"
            return 1
        fi
    fi
    
    # 检查许可证文件
    if ! ssh_exec "test -f ~/license.xml.sig" &>/dev/null; then
        log_warning "⚠️ 未找到许可证文件: ~/license.xml.sig"
        log_warning "安装后可能无法正常使用"
    else
        log_success "✅ 许可证文件存在"
    fi
    
    return 0
}

verify_after_install() {
    log_info "验证安装结果..."
    
    local success=true
    
    # 检查服务目录
    if ssh_exec "test -d /usr/local/cloud_nms/service" &>/dev/null; then
        log_success "✅ 服务目录已创建"
    else
        log_error "❌ 服务目录不存在"
        success=false
    fi
    
    # 检查服务进程
    echo ""
    log_info "=== 服务进程状态 ==="
    local process_count=$(ssh_exec "ps aux | grep -E 'maintenance-service|base-service|canal-service|file-service|gateway-service|log-service|message-service|nbi-service|olt-service|olt-adapter|onu-adapter|sw-adapter' | grep -v grep | wc -l" 2>/dev/null || echo "0")
    
    if [[ "$process_count" -gt 0 ]]; then
        log_success "✅ 运行中的服务进程: $process_count 个"
        ssh_exec "ps aux | grep -E 'base-service|gateway-service' | grep -v grep" 2>/dev/null || true
    else
        log_warning "⚠️ 未检测到运行中的服务进程"
        success=false
    fi
    
    # 检查 Web 访问
    echo ""
    log_info "=== Web 访问测试 ==="
    local http_code=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 -k "https://$SERVER_IP:31943" 2>/dev/null || echo "000")
    if [[ "$http_code" == "200" ]] || [[ "$http_code" == "302" ]]; then
        log_success "✅ Web 访问正常 (HTTPS $http_code)"
    else
        log_warning "⚠️ Web 访问异常 (HTTPS $http_code)"
        # 也测试 HTTP
        http_code=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 "http://$SERVER_IP/platform" 2>/dev/null || echo "000")
        if [[ "$http_code" == "200" ]] || [[ "$http_code" == "302" ]]; then
            log_success "✅ HTTP 访问正常 ($http_code)"
        fi
    fi
    
    $success
}

# ============================================
# 安装函数
# ============================================

install_fresh() {
    local version=$1
    
    log_info "执行全新安装 (版本: $version)..."
    
    log_info "[1/5] 解压并安装平台服务..."
    ssh_exec "
        cd ~ && \
        unzip -o CloudNMSPlatform_$version.zip && \
        chmod -R 755 CloudNMSPlatform_$version && \
        cd CloudNMSPlatform_$version && \
        sed -i 's|127.0.0.1|$SERVER_IP|' set_env.sh && \
        sed -i 's|language=zh|language=en|' set_env.sh && \
        sed -i 's|country=CN|country=US|' set_env.sh && \
        ./install_platform.sh
    "
    log_success "平台服务安装完成"
    
    log_info "[2/5] 复制许可证文件..."
    ssh_exec "cp ~/license.xml.sig /usr/local/cloud_nms/service/base-service" 2>/dev/null || log_warning "复制许可证失败，请手动处理"
    
    log_info "[3/5] 解压并安装业务服务..."
    ssh_exec "
        cd ~ && \
        unzip -o CloudNMSDummyBusiness_$version.zip && \
        chmod -R 755 CloudNMSDummyBusiness_$version && \
        cd CloudNMSDummyBusiness_$version && \
        sed -i 's|127.0.0.1|$SERVER_IP|' set_env.sh && \
        sed -i 's|language=zh|language=en|' set_env.sh && \
        sed -i 's|country=CN|country=US|' set_env.sh && \
        ./install_dummy_business.sh
    "
    log_success "业务服务安装完成"
    
    log_info "[4/5] 启动所有服务..."
    ssh_exec "cd ~/CloudNMSDummyBusiness_$version && ./start_all.sh"
    
    log_info "[5/5] 等待服务启动 (15秒)..."
    sleep 15
    
    log_success "服务安装完成！"
    
    # 初始化数据库
    echo ""
    init_database
}

install_lite() {
    local version=$1
    
    log_info "执行保留数据安装 (版本: $version)..."
    
    log_info "[1/4] 解压并升级平台服务..."
    ssh_exec "
        cd ~ && \
        unzip -o CloudNMSPlatform_$version.zip && \
        chmod -R 755 CloudNMSPlatform_$version && \
        cd CloudNMSPlatform_$version && \
        sed -i 's|127.0.0.1|$SERVER_IP|' set_env.sh && \
        sed -i 's|language=zh|language=en|' set_env.sh && \
        sed -i 's|country=CN|country=US|' set_env.sh && \
        ./install_platform_lite.sh
    "
    log_success "平台服务升级完成"
    
    log_info "[2/4] 复制许可证文件..."
    ssh_exec "cp ~/license.xml.sig /usr/local/cloud_nms/service/base-service" 2>/dev/null || log_warning "复制许可证失败，请手动处理"
    
    log_info "[3/4] 解压并升级业务服务..."
    ssh_exec "
        cd ~ && \
        unzip -o CloudNMSDummyBusiness_$version.zip && \
        chmod -R 755 CloudNMSDummyBusiness_$version && \
        cd CloudNMSDummyBusiness_$version && \
        sed -i 's|127.0.0.1|$SERVER_IP|' set_env.sh && \
        sed -i 's|language=zh|language=en|' set_env.sh && \
        sed -i 's|country=CN|country=US|' set_env.sh && \
        ./install_dummy_business_lite.sh
    "
    log_success "业务服务升级完成"
    
    log_info "[4/4] 启动所有服务..."
    ssh_exec "cd ~/CloudNMSDummyBusiness_$version && ./start_all.sh"
    
    log_info "等待服务启动 (15秒)..."
    sleep 15
    
    log_success "保留数据安装完成！"
}

# ============================================
# 数据库初始化
# ============================================

init_database() {
    log_info "初始化数据库用户..."
    
    # SQL 内容
    local sql_content="
-- 重置 admin 用户密码为 Genew1234
UPDATE nmsuser 
SET ifFirstLogin = false, 
    password = '54954cf34d9a328f6a9e650e300e610593aae5539146b9c35f0cc1b69e0d3103cf8ff36377c2d5943853748821ee80b62875cc14363ebf1a951afaee67ec9cb9', 
    passwordSalt = 'ili9gn0jtjhh16sh' 
WHERE id = 1;

-- 添加测试用户
INSERT INTO nmsuser (id, version, beEffective, createDate, creator, flag, ifSm, isLocked, loginFailNumber, password, passwordSalt, passwordModifyDate, passwordValidDays, reserved, userGroup_id, userName, ifSecondaryAuthConfirm, ifFirstLogin, timeZone, dateFormat, timeFormat, showModel, timeAndIpControlStrategy) 
VALUES
(2, 0, true, CURRENT_DATE, 'admin', '0:-1', false, false, 0, '1f5c449574a7120e801a4f281231b9fdae45da206d5647a52eadf835e18fd642c185330baa4bc667d95e4393a3d50d61b7b6c7b49457618076d2bdf48d6290cb', '6zfssrman3p41hsn', CURRENT_DATE, 180, false, -1, 'caowentao', false, false, 'default', 'yyyy-MM-dd', 'HH:mm:ss', 0, -1),
(5, 0, true, CURRENT_DATE, 'admin', '0:-1', false, false, 0, '271804146b3c455ad2e2aa98a4ffc2d3b9b58cdc039f2d85e79f5d9f5eda66b84f61d55c808fc1e5c7a2b23198ea13b6c4c4acfaa627b4e257aca440c56a2a62', 'gupwnjqmm6ghgorf', CURRENT_DATE, 180, false, -1, 'liucheng', false, false, 'default', 'yyyy-MM-dd', 'HH:mm:ss', 0, -1),
(7, 0, true, CURRENT_DATE, 'admin', '0:-1', false, false, 0, 'cc01072558f1be48ab633e658117d02b069629fd0a65c5d2af5fbce769da879c6f693cc18f2ce97351f68a0f6fd0bcdcb8ecd31b846828b6b506963c244d63f0', '3weymxz5shyky6qk', CURRENT_DATE, 180, false, -1, 'yangxinyuan', false, false, 'default', 'yyyy-MM-dd', 'HH:mm:ss', 0, -1),
(8, 0, true, CURRENT_DATE, 'admin', '0:-1', false, false, 0, '6590288491805cf8ed2d2a44c94da2ceb5b541335bae554bb8893ece3bb17de42437fc712ba3839c7478cb805d5d9a9e9980c2bd18ff210bb2bef4806c6fb139', '086v88cip971wm4b', CURRENT_DATE, 180, false, -1, 'qiyongfeng', false, false, 'default', 'yyyy-MM-dd', 'HH:mm:ss', 0, -1),
(9, 0, true, CURRENT_DATE, 'admin', '0:-1', false, false, 0, 'd5f345984c72c0ab9d896633bc172005f3134529e151156be5a423abfe5540df1e0ab5c31ad1864e35525184f33174219bd09c14ddf8f8996274d286c00fb4d4', 'cgiurnoy1pa0iar9', CURRENT_DATE, 180, false, -1, 'guohuihua', false, false, 'default', 'yyyy-MM-dd', 'HH:mm:ss', 0, -1),
(10, 0, true, CURRENT_DATE, 'admin', '0:-1', false, false, 0, '4086ec9c5a621c5ef67504ccd98ef997e48e2c988b8d031879347f7516ca6741835d5c9b30f81b36918b43a09810f98d0f06721c5d5ee400cc19999eb59aeb3e', 'dqxjy2fd8ag04vl3', CURRENT_DATE, 180, false, -1, 'panming', false, false, 'default', 'yyyy-MM-dd', 'HH:mm:ss', 0, -1)
ON DUPLICATE KEY UPDATE id=id;
"
    
    # 尝试多种 MySQL 路径
    local mysql_paths=(
        "/usr/local/cloud_nms/env/mysql/bin/mysql"
        "/usr/bin/mysql"
        "/usr/local/mysql/bin/mysql"
        "mysql"
    )
    
    for mysql_path in "${mysql_paths[@]}"; do
        log_info "尝试 MySQL 路径: $mysql_path"
        if echo "$sql_content" | ssh_exec "$mysql_path -u cloud_nms -p'$DB_PASSWORD' cloud_nms" 2>/dev/null; then
            log_success "✅ 数据库初始化完成"
            return 0
        fi
    done
    
    # 自动执行失败，生成手动指南
    log_warning "自动执行失败，生成手动执行指南..."
    
    # 上传 SQL 文件到服务器
    local sql_file="/tmp/init_cloudnms_users.sql"
    echo "$sql_content" > "$sql_file"
    scp_upload "$sql_file" "/tmp/"
    
    echo ""
    log_warning "=========================================="
    log_warning "  请手动执行数据库初始化"
    log_warning "=========================================="
    echo ""
    echo "SQL 文件已上传到服务器: /tmp/init_cloudnms_users.sql"
    echo ""
    echo "请执行以下命令:"
    echo ""
    echo "  ssh $SERVER_USER@$SERVER_IP"
    echo "  /usr/local/cloud_nms/env/mysql/bin/mysql -u cloud_nms -p'$DB_PASSWORD' cloud_nms < /tmp/init_cloudnms_users.sql"
    echo ""
    log_info "=========================================="
    
    return 1
}

# ============================================
# 主函数
# ============================================

show_usage() {
    cat << EOF
使用方法:
  $0 <version> <mode>
  $0 <version> --check    # 仅检查，不安装

参数说明:
  version    版本号，例如: 1.1.0.6
  mode       安装模式:
              - fresh: 全新安装（清空数据，初始化数据库）
              - lite: 保留数据安装（升级）

示例:
  $0 1.1.0.6 fresh    # 全新安装
  $0 1.1.0.6 lite     # 保留数据升级
  $0 1.1.0.6 --check  # 检查安装条件

EOF
}

main() {
    check_dependencies
    
    if [[ $# -lt 2 ]] || [[ "$1" == "-h" ]] || [[ "$1" == "--help" ]]; then
        show_usage
        exit 0
    fi
    
    local version=$1
    local mode=$2
    
    log_info "=========================================="
    log_info "  Cloud NMS 安装脚本"
    log_info "  版本: $version"
    log_info "  模式: $mode"
    log_info "  服务器: $SERVER_USER@$SERVER_IP"
    log_info "=========================================="
    
    # 安装前校验
    verify_before_install "$version" || exit 1
    
    if [[ "$mode" == "--check" ]]; then
        log_info "仅检查模式，不执行安装"
        exit 0
    fi
    
    # 执行安装
    echo ""
    case $mode in
        fresh)
            install_fresh "$version"
            ;;
        lite)
            install_lite "$version"
            ;;
        *)
            log_error "无效的安装模式: $mode"
            log_info "有效模式: fresh, lite"
            exit 1
            ;;
    esac
    
    # 安装后校验
    echo ""
    verify_after_install && {
        log_success "=========================================="
        log_success "  安装完成！"
        log_success "  登录账户: admin / Genew1234"
        log_success "  访问地址: https://$SERVER_IP:31943"
        log_success "=========================================="
    } || {
        log_warning "=========================================="
        log_warning "  安装可能不完全，请检查上述警告"
        log_warning "=========================================="
    }
}

main "$@"
