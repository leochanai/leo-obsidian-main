import json
import subprocess
import os
import sys

def load_servers(config_path="servers.json"):
    with open(config_path, 'r') as f:
        return json.load(f)

def stop_server(server):
    ip = server['ip']
    user = server['user']
    password = server['password']
    port = server.get('port', 22)
    
    print(f"[*] Connecting to {ip}...")

    # Enhanced shell command to handle VM shutdown gracefully
    # 1. Check if virsh exists
    # 2. Get running VMs
    # 3. Shutdown them and wait
    # 4. Shutdown host
    remote_cmd = """
if command -v virsh >/dev/null 2>&1; then
    echo "Checking for running VMs..."
    vms=$(virsh list --state-running --name)
    if [ -n "$vms" ]; then
        echo "Found running VMs: $vms"
        for vm in $vms; do 
            echo "Stopping VM: $vm"
            virsh shutdown $vm
        done
        
        echo "Waiting for VMs to shutdown (max 60s)..."
        count=0
        while [ -n "$(virsh list --state-running --name)" ] && [ $count -lt 20 ]; do
            sleep 3
            count=$((count+1))
            echo -n "."
        done
        echo ""
    else
        echo "No running VMs found."
    fi
else
    echo "virsh not found, skipping VM safety check."
fi
echo "Shutting down host..."
shutdown -h now
"""
    
    # Escape double quotes for the expect spawn command is tricky, 
    # so we will pass the command as a single argument to bash -c
    # But for expect readability/simplicity with complex multiline, 
    # it's often easier to just send the command line by line or use a here-doc approach in the remote shell if possible.
    # HOWEVER, to keep 'expect' simple, let's wrap the logic in a small script we execute, 
    # OR simpler: just assume bash is there and pass it as a long base64 string to avoid quote hell? 
    # No, that's overengineering. 
    # Let's clean up the remote_cmd to be a single line for "spawn ssh ..." arg, but that's hard.
    # Better approach: "Send" the commands once logged in? No, we need sudo/root.
    # The current script logs in as root.
    
    # Flatten checks for easier passing:
    cmd_flat = 'if command -v virsh >/dev/null; then for vm in $(virsh list --state-running --name); do virsh shutdown $vm; done; count=0; while [ -n "$(virsh list --state-running --name)" ] && [ $count -lt 20 ]; do sleep 3; ((count++)); done; fi; shutdown -h now'
    
    # Escape double quotes and dollar signs for TCL/Expect
    cmd_flat_escaped = cmd_flat.replace('"', '\\"').replace('$', '\\$')

    expect_script = f"""
set timeout 70
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
    
    # Write temp expect script
    tmp_script = f"temp_shutdown_{ip}.exp"
    with open(tmp_script, 'w') as f:
        f.write(expect_script)
    
    try:
        # Run expect
        result = subprocess.run(['expect', tmp_script], capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ [SUCCESS] Shutdown command sent to {ip}")
        elif result.returncode == 1:
            print(f"❌ [ERROR] Authentication failed for {ip}")
        elif result.returncode == 2:
            print(f"⚠️ [TIMEOUT] Connection or command timed out for {ip}")
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

    print("🚀 Starting Batch Server Shutdown Skill...")
    print("⚠️  Warning: This will shut down the remote hosts. Ensure VMs are configured to auto-suspend/shutdown.")
    
    servers = load_servers(config_path)
    
    for server in servers:
        stop_server(server)
        
    print("\n🏁 Process completed.")

if __name__ == "__main__":
    main()
