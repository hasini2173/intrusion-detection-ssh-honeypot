# System Workflow

## Workflow Steps

1. Attacker attempts SSH login to the honeypot server.
2. Cowrie SSH Honeypot captures login attempts.
3. Honeypot logs attacker activity:
   - Source IP
   - Username
   - Password
   - Commands executed
   - Timestamps
4. Log files are stored in JSON format.
5. Python analyzer parses logs.
6. Intrusion detection module identifies:
   - Brute-force attacks
   - Repeated login failures
   - Suspicious behavior
7. Explainable alert module generates alerts with:
   - Reason
   - Severity
   - Attack details
8. Visualization dashboard displays:
   - Top attacker IPs
   - Attack frequency
   - Security alerts

## Technologies Used

- Cowrie Honeypot
- Python
- Flask
- Pandas
- Matplotlib
- GitHub
