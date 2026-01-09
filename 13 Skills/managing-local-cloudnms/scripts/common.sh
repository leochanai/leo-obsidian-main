#!/bin/bash

# ============================================
# Cloud NMS 部署 - 公共配置和工具函数
# ============================================

# ============================================
# 配置参数
# ============================================

export SERVER_IP="192.168.0.98"
export SERVER_USER="cloud_nms"
export SERVER_PASSWORD="Genew1234"
export DB_PASSWORD="1Z_kF8s2mHcTnQHC"
export LOCAL_BUILD_PATH="/Users/farghost/IdeaProjects/HuahaiPlatform2/output"

# ============================================
# 颜色输出
# ============================================

export RED='\033[0;31m'
export GREEN='\033[0;32m'
export YELLOW='\033[1;33m'
export BLUE='\033[0;34m'
export NC='\033[0m' # No Color

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

scp_upload() {
    sshpass -p "$SERVER_PASSWORD" scp -o StrictHostKeyChecking=no "$1" "$SERVER_USER@$SERVER_IP:$2"
}

check_dependencies() {
    log_info "检查依赖工具..."
    if ! command -v sshpass &> /dev/null; then
        log_error "未找到 sshpass 工具，请先安装: brew install sshpass"
        exit 1
    fi
    log_success "依赖检查通过"
}

# 获取脚本所在目录
get_script_dir() {
    cd "$(dirname "${BASH_SOURCE[0]}")" && pwd
}
