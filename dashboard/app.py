from flask import Flask
import pandas as pd
import matplotlib.pyplot as plt
import os
plt.style.use('dark_background')

app = Flask(__name__)

LOG_FILE = "/home/nakka/cowrie/var/log/cowrie/cowrie.json"


@app.route("/")
def dashboard():

    if not os.path.exists(LOG_FILE):
        return "No logs found."

    # Read logs
    df = pd.read_json(LOG_FILE, lines=True)

    # Top attacker IPs
    ip_counts = df['src_ip'].value_counts().head(5)

    # Top usernames
    if 'username' in df.columns:
        username_counts = df['username'].value_counts().head(5)
    else:
        username_counts = pd.Series(dtype=int)

    # Top passwords
    if 'password' in df.columns:
        password_counts = df['password'].value_counts().head(5)
    else:
        password_counts = pd.Series(dtype=int)

    # Login attempts over time
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        time_counts = df.groupby(df['timestamp'].dt.minute).size()
    else:
        time_counts = pd.Series(dtype=int)

    # Generate graphs
    plt.figure(figsize=(14,10))

    # Graph 1 - Top IPs
    plt.subplot(2,2,1)
    ip_counts.plot(kind='bar', color='skyblue')
    plt.title("Top Attacker IPs")
    plt.xlabel("IP Address")
    plt.ylabel("Attempts")

    # Graph 2 - Usernames
    plt.subplot(2,2,2)
    username_counts.plot(kind='bar', color='orange')
    plt.title("Top Usernames")

    # Graph 3 - Passwords
    plt.subplot(2,2,3)
    password_counts.plot(kind='bar', color='red')
    plt.title("Top Passwords")

    # Graph 4 - Login attempts over time
    plt.subplot(2,2,4)
    time_counts.plot(kind='line', marker='o', color='green')
    plt.title("Login Attempts Over Time")
    plt.xlabel("Hour")
    plt.ylabel("Attempts")

    plt.tight_layout()

    # Save chart
    chart_path = "static/chart.png"

    os.makedirs("dashboard/static", exist_ok=True)

    plt.savefig(chart_path)

    total_attacks = int(ip_counts.sum())
    top_ip = ip_counts.idxmax()

    # HTML Dashboard
    html = f"""
    <html>

    <head>

    <title>SSH Honeypot Dashboard</title>

    <meta http-equiv="refresh" content="10">

    </head>

    <body style="
    font-family: Arial;
    background-color:#0f172a;
    color:white;
    padding:20px;
    ">

    <h1>🛡 SSH Honeypot SOC Dashboard</h1>

    <div style="
    display:flex;
    gap:20px;
    margin-bottom:20px;
    ">

        <div style="
        background:#1e293b;
        color:white;
        padding:20px;
        border-radius:10px;
        width:200px;
        ">

            <h3>Total Attacks</h3>

            <h2 style="color:red;">
            {total_attacks}
            </h2>

        </div>

        <div style="
        background:#1e293b;
        color:white;
        padding:20px;
        border-radius:10px;
        width:250px;
        ">

            <h3>Top Attacker IP</h3>

            <h2 style="color:skyblue;">
            {top_ip}
            </h2>

        </div>

        <div style="
        background:#1e293b;
        color:white;
        padding:20px;
        border-radius:10px;
        width:200px;
        ">

            <h3>Severity</h3>

            <h2 style="
            background:red;
            color:white;
            padding:8px;
            border-radius:8px;
            display:inline-block;
            ">
            HIGH
            </h2>

        </div>

    </div>

    <!-- Alert Box -->

    <div style="
    background:#3b0d0d;
    padding:15px;
    border-left:6px solid red;
    margin-bottom:20px;
    border-radius:10px;
    ">

        <h3>🚨 ALERT</h3>

        <p>
        Brute-force SSH attack detected from suspicious IP address.
        </p>

    </div>

    <!-- Alert Table -->

    <div style="
    background:#1e293b;
    padding:20px;
    border-radius:10px;
    margin-bottom:20px;
    ">

    <h2>Recent Alerts</h2>

    <table border="1"
    cellpadding="10"
    cellspacing="0"
    style="
    width:100%;
    border-collapse:collapse;
    color:white;
    ">

    <tr>
        <th>IP Address</th>
        <th>Severity</th>
        <th>Status</th>
    </tr>

    <tr>
        <td>{top_ip}</td>
        <td>HIGH</td>
        <td>Brute-force detected</td>
    </tr>

    </table>

    </div>

    <!-- Graph -->

    <div style="
    background:#1e293b;
    padding:20px;
    border-radius:10px;
    ">

        <h2>Attack Analytics</h2>

        <img src="/static/chart.png"
        width="100%">

    </div>
    <hr>
    <p style="color:gray;">
    SOC Monitoring Dasboard | SSH Honeypot IDS Project
    </p>

    <p style="color:gray;">
    Developed by: Hasini, Divya, Amulya
    </p>


    </body>
    </html>
    """

    return html


if __name__ == "__main__":
    app.run(debug=True)
