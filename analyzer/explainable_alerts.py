import json
from collections import Counter

log_file = "../../cowrie/var/log/cowrie/cowrie.json"

ips = []
passwords = []

with open(log_file) as f:
    for line in f:
        try:
            log = json.loads(line)

            if "src_ip" in log:
                ips.append(log["src_ip"])

            if "password" in log:
                passwords.append(log["password"])

        except:
            pass

ip_count = Counter(ips)
pass_count = Counter(passwords)

print("\n🔎 EXPLAINABLE ALERTS:\n")

# Brute-force explanation
for ip, count in ip_count.items():
    if count > 3:
        print(f"""
🚨 ALERT: Brute-force Attack Detected
IP Address: {ip}
Reason: {count} login attempts detected from same IP
Explanation: Multiple repeated login attempts indicate automated attack
Severity: HIGH
""")

# Password spraying explanation
for pwd, count in pass_count.items():
    if count > 2:
        print(f"""
⚠️ ALERT: Password Spraying Detected
Password: {pwd}
Reason: Same password used {count} times
Explanation: Attackers are trying common passwords across accounts
Severity: MEDIUM
""")
