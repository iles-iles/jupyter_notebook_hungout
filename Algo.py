#%%
import subprocess
import platform
import re


def get_arp_entries():
    if platform.system().lower() == "windows":
        output = subprocess.check_output("arp -a", shell=True).decode("cp1252", errors="ignore")

        # better Windows pattern
        pattern = r"(\d+\.\d+\.\d+\.\d+)\s+([0-9a-fA-F:-]{17,})"

    else:
        output = subprocess.check_output("arp -a", shell=True).decode("cp1252", errors="ignore")

        pattern = r"(\d+\.\d+\.\d+\.\d+)\s+.*?([0-9a-fA-F:]{17,})"

    matches = re.findall(pattern, output)
    return matches


arp_data = get_arp_entries()

clean = []

for ip, mac in arp_data:
    if (
        not ip.startswith("224.") and
        not ip.startswith("239.") and
        ip != "255.255.255.255"
    ):
        clean.append((ip, mac))

print("\nReal devices only:\n")

#%%
import socket

hostname = socket.gethostname()
ip_local = socket.gethostbyname(hostname)
#%%
import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()
for ip, mac in clean:
   G.add_edge(ip_local , ip)

plt.figure()
nx.draw(G, with_labels=True, node_size=2000)
plt.title("Local Network Graph")
plt.show()

