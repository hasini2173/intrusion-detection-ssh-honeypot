import json

log_file = "../../cowrie/var/log/cowrie/cowrie.json"

logs = []

with open(log_file) as f:
    for line in f:
        try:
            logs.append(json.loads(line))
        except:
            pass

print("Total logs:", len(logs))

ips = [log.get("src_ip") for log in logs if "src_ip" in log]
print("Unique IPs:", set(ips))

usernames = [log.get("username") for log in logs if "username" in log]
print("Usernames tried:", usernames[:5])

passwords = [log.get("password") for log in logs if "password" in log]
print("Passwords tried:", passwords[:5])

commands = [log.get("input") for log in logs if "input" in log]
print("Commands executed:", commands[:5])
