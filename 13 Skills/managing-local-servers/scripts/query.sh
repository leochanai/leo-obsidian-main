#!/bin/bash
# 服务器配置
SERVERS=(
    "192.168.0.91:root:genew1234"
    "192.168.0.95:root:genew1234"
    "192.168.2.235:root:root123"
)

# 报告文件
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPORT_FILE="$SCRIPT_DIR/report_query_$(date +%Y%m%d_%H%M%S).txt"

# 同时输出到屏幕和文件
exec > >(tee -a "$REPORT_FILE") 2>&1

echo "========================================"
echo "🔍 服务器状态查询报告"
echo "时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo "========================================"
echo ""

for entry in "${SERVERS[@]}"; do
    IFS=':' read -r ip user pass <<< "$entry"
    echo "┌──────────────────────────────────────"
    echo "│ 服务器: $ip"
    echo "└──────────────────────────────────────"
    
    expect << EOF 2>/dev/null
set timeout 10
log_user 1
spawn ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 $user@$ip "echo '主机名:' \$(hostname); echo '运行时间:' \$(uptime -p 2>/dev/null || uptime); echo ''; echo '虚拟机列表:'; virsh list --all 2>/dev/null || echo 'virsh 不可用'"
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
echo "🏁 查询完成"
echo "报告已保存: $REPORT_FILE"
echo "========================================"
