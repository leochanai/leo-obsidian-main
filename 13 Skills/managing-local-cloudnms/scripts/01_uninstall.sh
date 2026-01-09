#!/bin/bash

# ============================================
# Cloud NMS 部署 - 步骤 1: 卸载
# ============================================
# 用法: ./01_uninstall.sh
# 说明: 卸载现有 Cloud NMS 服务并清理文件
# ============================================

set -e

# 加载公共配置
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"

# ============================================
# 校验函数
# ============================================

verify_before_uninstall() {
    log_info "检查卸载前状态..."
    
    local has_service=false
    local has_packages=false
    
    # 检查服务目录
    if ssh_exec "test -d /usr/local/cloud_nms/service" &>/dev/null; then
        has_service=true
        log_info "✅ 检测到服务目录: /usr/local/cloud_nms/service"
        ssh_exec "ls -la /usr/local/cloud_nms/service/" 2>/dev/null || true
    else
        log_warning "⚠️ 服务目录不存在: /usr/local/cloud_nms/service"
    fi
    
    # 检查安装包
    if ssh_exec "ls ~/CloudNMSDummyBusiness_*.zip" &>/dev/null; then
        has_packages=true
        log_info "✅ 检测到安装包:"
        ssh_exec "ls -lh ~/CloudNMS*.zip" 2>/dev/null || true
    else
        log_warning "⚠️ 未检测到安装包"
    fi
    
    # 检查解压目录
    if ssh_exec "ls -d ~/CloudNMSPlatform_* ~/CloudNMSDummyBusiness_*" &>/dev/null 2>&1; then
        log_info "✅ 检测到解压目录:"
        ssh_exec "ls -d ~/CloudNMSPlatform_* ~/CloudNMSDummyBusiness_* 2>/dev/null" || true
    fi
    
    echo ""
    if ! $has_service && ! $has_packages; then
        log_warning "未检测到任何需要卸载的内容"
        return 1
    fi
    
    return 0
}

verify_after_uninstall() {
    log_info "验证卸载结果..."
    
    local success=true
    
    # 检查服务目录
    if ssh_exec "test -d /usr/local/cloud_nms/service && ls /usr/local/cloud_nms/service/*.jar" &>/dev/null 2>&1; then
        log_warning "⚠️ 服务目录仍存在 jar 文件"
        success=false
    else
        log_success "✅ 服务已清理"
    fi
    
    # 检查解压目录
    if ssh_exec "ls -d ~/CloudNMSPlatform_* ~/CloudNMSDummyBusiness_*" &>/dev/null 2>&1; then
        log_warning "⚠️ 解压目录仍存在"
        success=false
    else
        log_success "✅ 解压目录已清理"
    fi
    
    # 检查前端文件
    if ssh_exec "test -d /usr/local/cloud_nms/env/nginx/html/platform" &>/dev/null; then
        log_warning "⚠️ 前端文件仍存在"
        success=false
    else
        log_success "✅ 前端文件已清理"
    fi
    
    # 检查进程
    local process_count=$(ssh_exec "ps aux | grep -E 'base-service|gateway-service' | grep -v grep | wc -l" 2>/dev/null || echo "0")
    if [[ "$process_count" -gt 0 ]]; then
        log_warning "⚠️ 仍有 $process_count 个服务进程在运行"
        success=false
    else
        log_success "✅ 服务进程已停止"
    fi
    
    if $success; then
        return 0
    else
        return 1
    fi
}

# ============================================
# 卸载函数
# ============================================

uninstall_services() {
    log_warning "即将卸载所有 Cloud NMS 服务"
    if ! confirm "确认要卸载吗？此操作会删除所有服务和数据！"; then
        log_info "已取消卸载操作"
        return 1
    fi

    log_info "[1/4] 停止并卸载服务..."
    ssh_exec "cd /usr/local/cloud_nms/service/ && ./uninstall_all.sh" 2>/dev/null || log_warning "uninstall_all.sh 执行失败或服务不存在"
    
    log_info "[2/4] 清理解压目录..."
    ssh_exec "cd ~ && rm -rf CloudNMSDummyBusiness_*/ CloudNMSPlatform_*/" || log_warning "清理解压目录失败"
    
    log_info "[3/4] 清理前端文件..."
    ssh_exec "sudo rm -rf /usr/local/cloud_nms/env/nginx/html/platform /usr/local/cloud_nms/env/nginx/html/ems" || log_warning "清理前端文件失败"
    
    log_info "[4/4] 清理安装包（可选）..."
    if confirm "是否同时删除安装包 zip 文件？"; then
        ssh_exec "cd ~ && rm -f CloudNMS*.zip" || log_warning "清理安装包失败"
        log_success "安装包已清理"
    else
        log_info "保留安装包"
    fi
    
    log_success "卸载完成"
}

# ============================================
# 主函数
# ============================================

show_usage() {
    cat << EOF
使用方法:
  $0              # 交互式卸载
  $0 --check      # 仅检查状态，不执行卸载
  $0 --force      # 强制卸载，跳过确认

示例:
  $0
  $0 --check

EOF
}

main() {
    check_dependencies
    
    if [[ "$1" == "-h" ]] || [[ "$1" == "--help" ]]; then
        show_usage
        exit 0
    fi
    
    log_info "=========================================="
    log_info "  Cloud NMS 卸载脚本"
    log_info "  服务器: $SERVER_USER@$SERVER_IP"
    log_info "=========================================="
    
    # 卸载前校验
    verify_before_uninstall || {
        log_info "没有需要卸载的内容，退出"
        exit 0
    }
    
    if [[ "$1" == "--check" ]]; then
        log_info "仅检查模式，不执行卸载"
        exit 0
    fi
    
    # 执行卸载
    uninstall_services
    
    # 卸载后校验
    echo ""
    verify_after_uninstall && {
        log_success "=========================================="
        log_success "  卸载完成！"
        log_success "  下一步: ./02_upload.sh <version>"
        log_success "=========================================="
    } || {
        log_warning "=========================================="
        log_warning "  卸载可能不完全，请检查上述警告"
        log_warning "=========================================="
    }
}

main "$@"
