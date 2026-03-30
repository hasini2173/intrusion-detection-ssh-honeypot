import json
from collections import Counter

log_file = "../../cowrie/var/log/cowrie/cowrie.json"

ips = []
usernames = []
passwords = []

with open(log_file) as f:
    for line in f:
        try:
            log = json.loads(line)

            if "src_ip" in log:
                ips.append(log["src_ip"])

            if "username" in log:
                usernames.append(log["username"])

            if "password" in log:
                passwords.append(log["password"])

        except:
            pass

# Count occurrences
ip_count = Counter(ips)
user_count = Counter(usernames)
pass_count = Counter(passwords)

print("🔴 Top Attacker IPs:")
print(ip_count.most_common(5))

print("\n🔑 Most Tried Usernames:")
print(user_count.most_common(5))

print("\n🔐 Most Tried Passwords:")
print(pass_count.most_common(5))

# 🚨 Detection Rules
print("\n🚨 ALERTS:")

for ip, count in ip_count.items():
    if count > 3:
        print(f"⚠️ Brute-force attack detected from {ip} (Attempts: {count})")

for pwd, count in pass_count.items():
    if count > 2:
        print(f"⚠️ Password spraying detected: '{pwd}' used {count} times")

