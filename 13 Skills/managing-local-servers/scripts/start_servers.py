import json
import subprocess
import os
import sys

def load_servers(config_path="servers.json"):
    with open(config_path, 'r') as f:
        return json.load(f)

def start_vms(server):
    ip = server['ip']
    user = server['user']
    password = server['password']
    port = server.get('port', 22)
    target_vms = server.get('target_vms', [])
    vms_str = ' '.join(target_vms)

    print(f"[*] Connecting to {ip}...")
    print(f"    Target VMs: {vms_str if vms_str else 'All Shutoff VMs (Fallback)'}")

    # If target_vms is defined, we only check/start those.
    # If empty, we fallback to the old behavior (auto-start all shutoff) OR strictly do nothing?
    # Let's support the user's specific request: only start defined ones.
    
    if target_vms:
        # Construct a loop that checks each specific VM
        # We construct a bash array or just space separated string
        # "for vm in vm1 vm2; do ..."
        
        cmd_flat = f'if command -v virsh >/dev/null; then for vm in {vms_str}; do state=$(virsh domstate "$vm" 2>/dev/null || echo "notfound"); if [[ "$state" == "running" ]]; then echo "✅ $vm is running"; elif [[ "$state" == "shut off" ]]; then echo "🚀 Starting $vm..."; virsh start "$vm"; else echo "⚠️  $vm is in state: $state"; fi; done; virsh list --all; else echo "virsh not found"; fi'
    else
        # Fallback to old behavior: Start ALL shutoff VMs
        cmd_flat = 'if command -v virsh >/dev/null; then for vm in $(virsh list --state-shutoff --name); do virsh start $vm; done; virsh list --all; else echo "virsh not found"; fi'

    # Escape double quotes and dollar signs for TCL/Expect
    cmd_flat_escaped = cmd_flat.replace('"', '\\"').replace('$', '\\$')

    expect_script = f"""
set timeout 30
spawn ssh -p {port} -o StrictHostKeyChecking=no {user}@{ip} "{cmd_flat_escaped}"
expect {{
    -re "(?i)password:" {{
        send "{password}\\r"
        exp_continue
    }}
    "Permission denied" {{
        exit 1
    }}
    "s password:" {{
        send "{password}\\r"
        exp_continue
    }}
    timeout {{
        exit 2
    }}
    eof
}}
catch wait result
exit [lindex $result 3]
"""
    
    tmp_script = f"temp_start_{ip}.exp"
    with open(tmp_script, 'w') as f:
        f.write(expect_script)
    
    try:
        result = subprocess.run(['expect', tmp_script], capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ [SUCCESS] Start commands executed on {ip}")
            # print(result.stdout) # Optional: print details
        elif result.returncode == 1:
            print(f"❌ [ERROR] Authentication failed for {ip}")
        elif result.returncode == 2:
            print(f"⚠️ [TIMEOUT] Connection timed out for {ip} (Host might be down)")
        else:
            print(f"❌ [ERROR] Unknown error for {ip}")
            
    except Exception as e:
        print(f"❌ [EXCEPTION] {e}")
    finally:
        if os.path.exists(tmp_script):
            os.remove(tmp_script)

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, "servers.json")
    
    if not os.path.exists(config_path):
        print(f"Error: {config_path} not found.")
        return

    print("🚀 Starting Batch VM Startup...")
    print("ℹ️  Note: This script requires physical servers to be powered ON already.")
    
    servers = load_servers(config_path)
    
    for server in servers:
        start_vms(server)
        
    print("🏁 Process completed.")

if __name__ == "__main__":
    main()
