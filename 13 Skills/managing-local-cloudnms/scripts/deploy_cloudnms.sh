#!/bin/bash

# ============================================
# Cloud NMS 部署脚本（主入口）
# ============================================
# 此脚本调用拆分后的子脚本完成完整部署流程
# 也可以直接使用子脚本进行单步操作
# ============================================

set -e

# 获取脚本目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 加载公共配置
source "$SCRIPT_DIR/common.sh"

# ============================================
# 查看日志
# ============================================

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
    echo ""
    echo "  独立脚本（推荐单步调试）:"
    echo "    ./01_uninstall.sh             卸载服务"
    echo "    ./02_upload.sh <version>      上传安装包"
    echo "    ./03_install.sh <version> fresh 全新安装"
    echo "    ./03_install.sh <version> lite  保留数据升级"
    echo ""
    echo -e "${BLUE}--------------------------------------${NC}"
    echo "  菜单选项:"
    echo "  1) 卸载服务"
    echo "  2) 上传安装包"
    echo "  3) 全新安装 (安装 + 数据库初始化)"
    echo "  4) 保留数据安装 (升级)"
    echo "  5) 完整流程 (卸载 + 上传 + 全新安装)"
    echo "  6) 查看实时日志"
    echo "  0) 退出"
    echo -e "${BLUE}======================================${NC}"
}

show_usage() {
    cat << EOF
使用方法:
  交互式模式:
    $0

  命令行模式（完整流程）:
    $0 <version> <mode>

  单步执行（推荐调试）:
    ./01_uninstall.sh                # 卸载服务
    ./02_upload.sh <version>         # 上传安装包
    ./03_install.sh <version> fresh  # 全新安装
    ./03_install.sh <version> lite   # 保留数据升级

参数说明:
  version    版本号，例如: 1.1.0.6
  mode       安装模式:
              - fresh: 全新安装（清空数据）
              - lite: 保留数据安装（升级）

示例:
  $0 1.1.0.6 fresh         # 上传 + 全新安装
  $0 1.1.0.6 lite          # 上传 + 保留数据升级

EOF
}

interactive_mode() {
    while true; do
        show_menu
        read -p "请选择操作 [0-6]: " choice
        
        case $choice in
            1)
                "$SCRIPT_DIR/01_uninstall.sh"
                ;;
            2)
                read -p "请输入版本号 (例如 1.1.0.6): " version
                while [[ -z "$version" ]]; do
                    log_error "版本号不能为空！"
                    read -p "请输入版本号: " version
                done
                "$SCRIPT_DIR/02_upload.sh" "$version"
                ;;
            3)
                read -p "请输入版本号 (例如 1.1.0.6): " version
                while [[ -z "$version" ]]; do
                    log_error "版本号不能为空！"
                    read -p "请输入版本号: " version
                done
                "$SCRIPT_DIR/03_install.sh" "$version" fresh
                ;;
            4)
                read -p "请输入版本号 (例如 1.1.0.6): " version
                while [[ -z "$version" ]]; do
                    log_error "版本号不能为空！"
                    read -p "请输入版本号: " version
                done
                "$SCRIPT_DIR/03_install.sh" "$version" lite
                ;;
            5)
                read -p "请输入版本号 (例如 1.1.0.6): " version
                while [[ -z "$version" ]]; do
                    log_error "版本号不能为空！"
                    read -p "请输入版本号: " version
                done
                "$SCRIPT_DIR/01_uninstall.sh"
                "$SCRIPT_DIR/02_upload.sh" "$version"
                "$SCRIPT_DIR/03_install.sh" "$version" fresh
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
            "$SCRIPT_DIR/02_upload.sh" "$version"
            "$SCRIPT_DIR/03_install.sh" "$version" fresh
            ;;
        lite)
            log_info "命令行模式: 保留数据安装 $version"
            "$SCRIPT_DIR/02_upload.sh" "$version"
            "$SCRIPT_DIR/03_install.sh" "$version" lite
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
