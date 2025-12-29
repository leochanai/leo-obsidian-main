import json
import subprocess
import os
import sys

def load_servers(config_path="servers.json"):
    with open(config_path, 'r') as f:
        return json.load(f)

def query_server(server):
    ip = server['ip']
    user = server['user']
    password = server['password']
    port = server.get('port', 22)
    
    print(f"[*] Connecting to {ip}...")

    # Remote command to only query status
    remote_cmd = """
echo "=== Host Info ==="
hostname
uptime
echo ""
if command -v virsh >/dev/null 2>&1; then
    echo "=== Virtual Machines (virsh) ==="
    virsh list --all
else
    echo "⚠️  virsh command not found on this host."
fi
"""
    
    # We pass the command as a single argument to bash does not work well directly in expect spawn string due to escaping.
    # We will stick to the same pattern: sending the command line by line or using a simpler one-liner.
    # For robust output capturing, let's keep it simple.
    
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
    
    tmp_script = f"temp_query_{ip}.exp"
    with open(tmp_script, 'w') as f:
        f.write(expect_script)
    
    try:
        # Run expect and capture output
        result = subprocess.run(['expect', tmp_script], capture_output=True, text=True)
        
        # Clean up output: remove the ssh login banner/password prompt lines if possible or just show all
        # Expect output usually contains the specific interaction. 
        # We can just print the stdout.
        
        if result.returncode == 0:
            print(f"✅ [SUCCESS] {ip} Status:")
            # Filter output to hide the expect/ssh noise if possible, but raw is fine for now
            # The output will contain the password prompt and send, which is a bit ugly but acceptable for internal tool.
            # To clean it up, we'd need more complex expect regex or python paramiko. 
            # Sticking to expect as requested by previous pattern.
            print("---------------------------------------------------")
            print(result.stdout.strip())
            print("---------------------------------------------------\n")
        elif result.returncode == 1:
            print(f"❌ [ERROR] Authentication failed for {ip}")
            print("--- Debug Output (STDOUT) ---")
            print(result.stdout)
            print("--- Debug Output (STDERR) ---")
            print(result.stderr)
            print("-----------------------------")
        elif result.returncode == 2:
            print(f"⚠️ [TIMEOUT] Connection timed out for {ip}")
            print(result.stdout)
        else:
            print(f"❌ [ERROR] Unknown error for {ip}: {result.stderr}")
            
    except Exception as e:
        print(f"❌ [EXCEPTION] Failed to run script for {ip}: {e}")
    finally:
        if os.path.exists(tmp_script):
            os.remove(tmp_script)

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, "servers.json")
    
    if not os.path.exists(config_path):
        print(f"Error: {config_path} not found.")
        return

    print("🔍 Starting Batch Server Query (Safe Mode)...")
    
    servers = load_servers(config_path)
    
    for server in servers:
        query_server(server)
        
    print("🏁 Query completed.")

if __name__ == "__main__":
    main()
