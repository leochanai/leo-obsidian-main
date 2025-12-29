#!/bin/bash
# 服务器配置
SERVERS=(
    "192.168.0.91:root:genew1234"
    "192.168.0.95:root:genew1234"
    "192.168.2.235:root:root123"
)

# 报告文件
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPORT_FILE="$SCRIPT_DIR/report_stop_$(date +%Y%m%d_%H%M%S).txt"

exec > >(tee -a "$REPORT_FILE") 2>&1

echo "========================================"
echo "🛑 服务器安全关机报告"
echo "时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo "⚠️  流程: 关闭VM -> 等待30秒 -> 关闭物理机"
echo "========================================"
echo ""

for entry in "${SERVERS[@]}"; do
    IFS=':' read -r ip user pass <<< "$entry"
    
    echo "┌──────────────────────────────────────"
    echo "│ 服务器: $ip"
    echo "└──────────────────────────────────────"
    
    expect << EOF 2>/dev/null
set timeout 60
spawn ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 $user@$ip "echo '正在关闭虚拟机...'; for vm in \$(virsh list --state-running --name 2>/dev/null); do echo \"关闭: \$vm\"; virsh shutdown \$vm; done; echo '等待30秒...'; sleep 30; echo '关闭物理机...'; /sbin/shutdown -h now"
expect {
    -re "(?i)password:" { send "$pass\r"; exp_continue }
    timeout { puts "连接超时（可能已关机）"; exit 0 }
    eof
}
EOF
    
    echo "✅ 关机指令已发送"
    echo ""
done

echo "========================================"
echo "🏁 所有关机指令已发送"
echo "报告已保存: $REPORT_FILE"
echo "========================================"
