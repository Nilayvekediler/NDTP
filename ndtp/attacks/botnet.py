from django.http import HttpResponse
from proxmoxer import ProxmoxAPI
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import time
import attacksRun

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

proxmox = ProxmoxAPI('192.168.1.104', user='root@pam', password='nıla123', verify_ssl=False)

# Örnek olarak cluster üzerindeki sanal makineleri listeleme
cluster_nodes = proxmox.cluster.resources.get(type='node')

for node in cluster_nodes:
    print("Node:", node['node'])
    for ct in proxmox.nodes(node['node']).lxc.get():
        print(" - CT ID:", ct['vmid']+" - CT:", ct['name'])

# CT başlatma işlemi
node_name = "proxmoxmonster"
ct_id = 100

try:
    proxmox.nodes(node_name).lxc(ct_id).status.start.post()
    print("CT başlatıldı.")
except proxmox.ResourceException as e:
    print("CT başlatma hatası:", str(e))

try:
    proxmox.nodes(node_name).lxc(ct_id).status.stop.post()
    print("CT durduruldu.")
except proxmox.ResourceException as e:
    print("CT durdurma hatası:", str(e))

# def start_ct(request, node, ct_id,arcode):
#     try:
#         proxmox.nodes(node).lxc(ct_id).status.start.post()
#         time.sleep(10)  # Başlarsa bu bekleme süresini yapabilirsiniz

#         python_script = attacksRun.arcode
#         attacksRun.run_python_script_on_ct(node, ct_id, python_script)
#         #attacksRun.run_command_on_ct(node, ct_id, "python synFlood.py") #ÇALIŞIYOR

#         #return HttpResponse("CT başlatıldı.")
#         return HttpResponse("Saldırı başlatıldı.")
    
#     except proxmox.ResourceException as e:
#         return HttpResponse("CT başlatma hatası: " + str(e))