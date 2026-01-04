import json
import subprocess
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

# 用于线程安全的临时文件计数器
_file_counter = 0
_file_lock = threading.Lock()

def load_servers(config_path="servers.json"):
    with open(config_path, 'r') as f:
        return json.load(f)

def get_unique_script_name(ip):
    """生成线程安全的唯一临时脚本文件名"""
    global _file_counter
    with _file_lock:
        _file_counter += 1
        return f"temp_query_{ip}_{_file_counter}_{threading.current_thread().ident}.exp"

def query_server(server):
    """
    查询单台服务器状态，返回结果字典而非直接打印。
    支持并发调用。
    """
    ip = server['ip']
    user = server['user']
    password = server['password']
    port = server.get('port', 22)
    
    result_data = {
        'ip': ip,
        'status': 'unknown',
        'output': '',
        'error': ''
    }

    cmd_flat = 'echo "--- Host: $(hostname) ---"; uptime; if command -v virsh >/dev/null; then echo "--- VMs ---"; virsh list --all; else echo "No virsh found"; fi'
    
    # Escape double quotes for TCL/Expect
    cmd_flat_escaped = cmd_flat.replace('"', '\\"').replace('$', '\\$')

    expect_script = f"""
set timeout 10
spawn ssh -p {port} -o StrictHostKeyChecking=no {user}@{ip} "{cmd_flat_escaped}"
expect {{
    -re "(?i)password:" {{
        send "{password}\\r"
        exp_continue
    }}
    "Permission denied" {{
        exit 1
    }}
    timeout {{
        exit 2
    }}
    eof
}}
catch wait result
exit [lindex $result 3]
"""
    
    tmp_script = get_unique_script_name(ip)
    with open(tmp_script, 'w') as f:
        f.write(expect_script)
    
    try:
        # Run expect and capture output
        result = subprocess.run(['expect', tmp_script], capture_output=True, text=True)
        
        if result.returncode == 0:
            result_data['status'] = 'success'
            result_data['output'] = result.stdout.strip()
        elif result.returncode == 1:
            result_data['status'] = 'auth_failed'
            result_data['output'] = result.stdout
            result_data['error'] = result.stderr
        elif result.returncode == 2:
            result_data['status'] = 'timeout'
            result_data['output'] = result.stdout
        else:
            result_data['status'] = 'error'
            result_data['error'] = result.stderr
            
    except Exception as e:
        result_data['status'] = 'exception'
        result_data['error'] = str(e)
    finally:
        if os.path.exists(tmp_script):
            os.remove(tmp_script)
    
    return result_data

def print_result(result_data):
    """格式化输出单个服务器的查询结果"""
    ip = result_data['ip']
    status = result_data['status']
    
    if status == 'success':
        print(f"✅ [SUCCESS] {ip} Status:")
        print("---------------------------------------------------")
        print(result_data['output'])
        print("---------------------------------------------------\n")
    elif status == 'auth_failed':
        print(f"❌ [ERROR] Authentication failed for {ip}")
        print("--- Debug Output (STDOUT) ---")
        print(result_data['output'])
        print("--- Debug Output (STDERR) ---")
        print(result_data['error'])
        print("-----------------------------")
    elif status == 'timeout':
        print(f"⚠️ [TIMEOUT] Connection timed out for {ip}")
        print(result_data['output'])
    elif status == 'exception':
        print(f"❌ [EXCEPTION] Failed to run script for {ip}: {result_data['error']}")
    else:
        print(f"❌ [ERROR] Unknown error for {ip}: {result_data['error']}")

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, "servers.json")
    
    if not os.path.exists(config_path):
        print(f"Error: {config_path} not found.")
        return

    servers = load_servers(config_path)
    server_count = len(servers)
    
    print(f"🔍 Starting Concurrent Server Query ({server_count} servers)...")
    print(f"📡 Querying all servers in parallel...\n")
    
    # 使用线程池并发查询所有服务器
    results = []
    with ThreadPoolExecutor(max_workers=server_count) as executor:
        # 提交所有任务
        future_to_server = {executor.submit(query_server, server): server for server in servers}
        
        # 收集结果（按完成顺序）
        for future in as_completed(future_to_server):
            server = future_to_server[future]
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                results.append({
                    'ip': server['ip'],
                    'status': 'exception',
                    'output': '',
                    'error': str(e)
                })
    
    # 按 IP 排序后统一输出，保持一致的输出顺序
    results.sort(key=lambda x: x['ip'])
    
    print("=" * 60)
    print("📊 Query Results Summary")
    print("=" * 60 + "\n")
    
    for result in results:
        print_result(result)
    
    # 输出统计信息
    success_count = sum(1 for r in results if r['status'] == 'success')
    failed_count = server_count - success_count
    
    print("=" * 60)
    print(f"🏁 Query completed: {success_count}/{server_count} succeeded", end="")
    if failed_count > 0:
        print(f", {failed_count} failed")
    else:
        print()
    print("=" * 60)

if __name__ == "__main__":
    main()
