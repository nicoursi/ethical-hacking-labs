#!/usr/bin/env python3
from scapy.all import *
from search_iface_by_prefx import *
  
interface = search_iface_by_prefx("br-", get_if_list())
print (f'the interface is {interface}')

def print_pkt(pkt):
    print (f'TCP packet received from {pkt[IP].src} to {pkt[IP].dst}')
    pkt[TCP].show()

pkt = sniff(iface=interface, filter='tcp dst port 23 and src host 10.9.0.6', prn=print_pkt)
