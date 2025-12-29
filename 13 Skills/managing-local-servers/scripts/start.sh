#!/bin/bash
# 服务器配置
SERVERS=(
    "192.168.0.91:root:genew1234"
    "192.168.0.95:root:genew1234"
    "192.168.2.235:root:root123"
)

# 需要启动的虚拟机列表
declare -A TARGET_VMS
TARGET_VMS["192.168.0.91"]="Win7N2-0.94 rhel7.3N1_0.92"
TARGET_VMS["192.168.0.95"]="Centos7.9-98 rh-vm1-96 rh-vm2-97"
TARGET_VMS["192.168.2.235"]="rh7.9-2.118 rh7.9-2.117 rh7.9-2.120 rh7.9-2.127"

# 报告文件
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPORT_FILE="$SCRIPT_DIR/report_start_$(date +%Y%m%d_%H%M%S).txt"

exec > >(tee -a "$REPORT_FILE") 2>&1

echo "========================================"
echo "🚀 虚拟机启动报告"
echo "时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo "========================================"
echo ""

for entry in "${SERVERS[@]}"; do
    IFS=':' read -r ip user pass <<< "$entry"
    vms="${TARGET_VMS[$ip]}"
    
    echo "┌──────────────────────────────────────"
    echo "│ 服务器: $ip"
    echo "│ 目标VM: $vms"
    echo "└──────────────────────────────────────"
    
    expect << EOF 2>/dev/null
set timeout 30
spawn ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 $user@$ip "for vm in $vms; do echo \"启动: \$vm\"; virsh start \$vm 2>&1; done; echo ''; echo '当前状态:'; virsh list --all"
expect {
    -re "(?i)password:" { send "$pass\r"; exp_continue }
    timeout { puts "连接超时"; exit 1 }
    eof
}
EOF
    
    if [ $? -ne 0 ]; then
        echo "❌ 连接失败"
    fi
    echo ""
done

echo "========================================"
echo "🏁 启动完成"
echo "报告已保存: $REPORT_FILE"
echo "========================================"
