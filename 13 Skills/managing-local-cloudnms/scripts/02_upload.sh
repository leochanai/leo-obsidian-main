#!/bin/bash

# ============================================
# Cloud NMS 部署 - 步骤 2: 上传安装包
# ============================================
# 用法: ./02_upload.sh <version>
# 示例: ./02_upload.sh 1.1.0.6
# ============================================

set -e

# 加载公共配置
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"

# ============================================
# 校验函数
# ============================================

verify_local_packages() {
    local version=$1
    
    log_info "检查本地安装包..."
    
    local platform_pkg="$LOCAL_BUILD_PATH/CloudNMSPlatform_$version.zip"
    local business_pkg="$LOCAL_BUILD_PATH/CloudNMSDummyBusiness_$version.zip"
    
    if [[ ! -f "$platform_pkg" ]]; then
        log_error "❌ 平台安装包不存在: $platform_pkg"
        return 1
    fi
    log_success "✅ 平台安装包: $(ls -lh "$platform_pkg" | awk '{print $5}')"
    
    if [[ ! -f "$business_pkg" ]]; then
        log_error "❌ 业务安装包不存在: $business_pkg"
        return 1
    fi
    log_success "✅ 业务安装包: $(ls -lh "$business_pkg" | awk '{print $5}')"
    
    return 0
}

verify_remote_packages() {
    local version=$1
    
    log_info "检查服务器上的安装包..."
    
    local has_platform=false
    local has_business=false
    
    if ssh_exec "test -f ~/CloudNMSPlatform_$version.zip" &>/dev/null; then
        has_platform=true
        log_success "✅ 服务器已有: CloudNMSPlatform_$version.zip"
    else
        log_info "⏳ 待上传: CloudNMSPlatform_$version.zip"
    fi
    
    if ssh_exec "test -f ~/CloudNMSDummyBusiness_$version.zip" &>/dev/null; then
        has_business=true
        log_success "✅ 服务器已有: CloudNMSDummyBusiness_$version.zip"
    else
        log_info "⏳ 待上传: CloudNMSDummyBusiness_$version.zip"
    fi
    
    if $has_platform && $has_business; then
        return 0  # 都已存在
    fi
    return 1  # 需要上传
}

verify_after_upload() {
    local version=$1
    
    log_info "验证上传结果..."
    
    local success=true
    
    if ssh_exec "test -f ~/CloudNMSPlatform_$version.zip" &>/dev/null; then
        local size=$(ssh_exec "ls -lh ~/CloudNMSPlatform_$version.zip | awk '{print \$5}'" 2>/dev/null)
        log_success "✅ CloudNMSPlatform_$version.zip ($size)"
    else
        log_error "❌ CloudNMSPlatform_$version.zip 上传失败"
        success=false
    fi
    
    if ssh_exec "test -f ~/CloudNMSDummyBusiness_$version.zip" &>/dev/null; then
        local size=$(ssh_exec "ls -lh ~/CloudNMSDummyBusiness_$version.zip | awk '{print \$5}'" 2>/dev/null)
        log_success "✅ CloudNMSDummyBusiness_$version.zip ($size)"
    else
        log_error "❌ CloudNMSDummyBusiness_$version.zip 上传失败"
        success=false
    fi
    
    $success
}

# ============================================
# 上传函数
# ============================================

upload_packages() {
    local version=$1
    
    log_info "[1/2] 上传 CloudNMSPlatform_$version.zip..."
    scp_upload "$LOCAL_BUILD_PATH/CloudNMSPlatform_$version.zip" "~/"
    
    log_info "[2/2] 上传 CloudNMSDummyBusiness_$version.zip..."
    scp_upload "$LOCAL_BUILD_PATH/CloudNMSDummyBusiness_$version.zip" "~/"
    
    log_success "上传完成"
}

# ============================================
# 主函数
# ============================================

show_usage() {
    cat << EOF
使用方法:
  $0 <version>          # 上传安装包
  $0 <version> --check  # 仅检查，不上传
  $0 <version> --force  # 强制重新上传

参数说明:
  version    版本号，例如: 1.1.0.6

示例:
  $0 1.1.0.6
  $0 1.1.0.6 --check
  $0 1.1.0.6 --force

EOF
}

main() {
    check_dependencies
    
    if [[ $# -lt 1 ]] || [[ "$1" == "-h" ]] || [[ "$1" == "--help" ]]; then
        show_usage
        exit 0
    fi
    
    local version=$1
    local check_only=false
    local force_upload=false
    
    if [[ "$2" == "--check" ]]; then
        check_only=true
    elif [[ "$2" == "--force" ]]; then
        force_upload=true
    fi
    
    log_info "=========================================="
    log_info "  Cloud NMS 上传脚本"
    log_info "  版本: $version"
    log_info "  服务器: $SERVER_USER@$SERVER_IP"
    log_info "=========================================="
    
    # 检查本地包
    verify_local_packages "$version" || exit 1
    
    # 检查远程包
    echo ""
    if verify_remote_packages "$version" && ! $force_upload; then
        log_success "服务器已有该版本安装包"
        if ! $check_only && confirm "是否重新上传？"; then
            force_upload=true
        else
            log_info "跳过上传"
            log_success "=========================================="
            log_success "  下一步: ./03_install.sh $version fresh"
            log_success "=========================================="
            exit 0
        fi
    fi
    
    if $check_only; then
        log_info "仅检查模式，不执行上传"
        exit 0
    fi
    
    # 执行上传
    echo ""
    upload_packages "$version"
    
    # 验证上传
    echo ""
    verify_after_upload "$version" && {
        log_success "=========================================="
        log_success "  上传成功！"
        log_success "  下一步: ./03_install.sh $version fresh"
        log_success "=========================================="
    } || {
        log_error "=========================================="
        log_error "  上传失败，请检查网络连接"
        log_error "=========================================="
        exit 1
    }
}

main "$@"
