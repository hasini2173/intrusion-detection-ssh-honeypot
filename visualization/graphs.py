import matplotlib.pyplot as plt

ips = ["127.0.0.1"]
attempts = [22]

plt.bar(ips, attempts)
plt.title("Top Attacker IPs")
plt.xlabel("IP Address")
plt.ylabel("Attempts")

plt.savefig("attack_graph.png")
print("Graph generated successfully.")
