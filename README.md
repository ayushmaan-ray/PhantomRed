# PhantomRed 🔴
> Red Team Command & Control (C2) Simulator with Persistence Mechanism

---

## ⚠️ Disclaimer
This project is developed **strictly for educational and research purposes**.  
It is intended to simulate Red Team concepts within **controlled lab environments only**.  
Do not deploy on systems without **explicit authorization**.  
The author is not responsible for any misuse of this tool.

---

## 📌 Overview
PhantomRed is a Python-based simulation of a Red Team Command & Control (C2) framework.  
It demonstrates how attackers establish remote access, execute commands on a target system,  
maintain persistence across reboots, and log session data — all within a safe, ethical lab environment.

Built to understand offensive security concepts, not to cause harm.

---

## 🏗️ Architecture

```
PhantomRed/
│
├── server/
│   └── c2_server.py        # Attacker-side controller
│
├── agent/
│   ├── agent.py            # Target-side agent
│   └── persistence.py      # Cron-based persistence module
│
├── target_info/            # Auto-generated session logs
│   └── user_YYYY-MM-DD_HH-MM-SS.txt
│
└── README.md
```

| Component | Role |
|---|---|
| `c2_server.py` | Listens for agent connections, receives recon, sends commands, logs sessions |
| `agent.py` | Connects back to server, runs auto recon, executes commands, installs persistence |
| `persistence.py` | Adds agent to crontab for automatic reboot survival |
| `target_info/` | Stores timestamped session logs per target |

---

## 🔴 Attack Lifecycle Context

PhantomRed simulates stages 3–4 of the Red Team attack lifecycle:

```
[1] Reconnaissance
[2] Initial Access
[3] ✅ Persistence          ← persistence.py     (MITRE ATT&CK: T1053)
[4] ✅ C2 Communication     ← c2_server.py + agent.py  (MITRE ATT&CK: T1059)
[5] Privilege Escalation
[6] Lateral Movement
[7] Exfiltration
```

---

## ⚙️ Features
- TCP socket-based C2 communication channel (reverse connection pattern)
- Remote command execution on target system with real-time output
- Automatic system recon on first connect — user, OS, IP, privilege level
- Agent retry loop — reconnects every 30s if server is offline
- Automatic persistence via Linux crontab (`@reboot`) on first run
- Duplicate persistence check — won't install twice
- Timestamped session logging to `target_info/` folder
- Graceful error handling for invalid or failed commands
- ASCII banner with color output

---

## 🚀 Setup & Usage

**Requirements**
- Python 3.x
- Linux (tested on Kali Linux VM)
- Lab environment only (two terminals or two VMs)

**Step 1 — Start the C2 Server**
```bash
cd server/
python3 c2_server.py
```

**Step 2 — Start the Agent (on target machine)**
```bash
cd agent/
python3 agent.py
```

**Step 3 — Agent connects and sends auto recon**
```
[*] C2 Server listening on 0.0.0.0:4444
[+] Agent connected from 127.0.0.1:52922
[Agent]:
===== SYSTEM RECON =====
[User]    : moshis
[PWD]     : /home/moshis/PhantomRed/agent
[OS]      : Linux Moshis 6.18.3+kali1-amd64 x86_64 GNU/Linux
[IP]      : 10.0.2.15 172.17.0.1
[ID]      : uid=1000(moshis) gid=1000(moshis) groups=1000(moshis),27(sudo)
========================
File saved
[C2]>
```

**Step 4 — Send commands from server**
```
[C2]> whoami
[Agent]: moshis

[C2]> pwd
[Agent]: /home/moshis/PhantomRed/agent

[C2]> ls -la
[Agent]: agent.py  persistence.py  __pycache__
```

**Step 5 — Session log is auto-saved**
```bash
cat target_info/moshis_2026-03-07_02-25-10.txt
```
```
===== SYSTEM RECON =====
[User]    : moshis
...
========================

[CMD]: whoami
[OUT]: moshis

[CMD]: ls -la
[OUT]: agent.py  persistence.py  __pycache__
```

**Persistence verification**
```bash
crontab -l
# Output: @reboot python3 /home/moshis/PhantomRed/agent/agent.py
```

**Agent retry behavior (server offline)**
```
[!] Server unavailable, retrying in 30s...
[!] Server unavailable, retrying in 30s...
[+] Connected to C2 server
```

---

## 📚 Educational Notes
- C2 frameworks are used by Red Teams to simulate real attacker behavior
- This project uses the **reverse connection** pattern — agent initiates outbound connection to server, evading basic inbound firewalls
- Cron-based persistence (`@reboot`) is a real technique used by Linux malware — mapped to MITRE ATT&CK T1053
- Remote command execution maps to MITRE ATT&CK T1059
- Session logging mirrors real operator tradecraft — reviewing output after a session
- Safe commands only — no payloads, no exploitation, no AV evasion

---

## 👤 Author
**Ayushman Ray**
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/ayushman-ray-16b265251/)

