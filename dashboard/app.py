from flask import Flask
import pandas as pd
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

LOG_FILE = "../../cowrie/var/log/cowrie/cowrie.json"

@app.route("/")
def dashboard():

    if not os.path.exists(LOG_FILE):
        return "No logs found."

    df = pd.read_json(LOG_FILE, lines=True)

    ip_counts = df['src_ip'].value_counts().head(5)

    plt.figure(figsize=(8,5))
    ip_counts.plot(kind='bar')

    plt.title("Top Attacker IPs")
    plt.xlabel("IP Address")
    plt.ylabel("Attempts")

    chart_path = "static/chart.png"

    os.makedirs("static", exist_ok=True)

    plt.savefig(chart_path)

    html = f"""
    <h1>SSH Honeypot Dashboard</h1>

    <h2>Top Attacker IPs</h2>

    <img src="/static/chart.png" width="700">
    """

    return html

if __name__ == "__main__":
    app.run(debug=True)
