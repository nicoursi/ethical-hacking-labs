#!/usr/bin/env python3
from scapy.all import *
from search_iface_by_prefx import *
  
interface = search_iface_by_prefx("br-", get_if_list())
print (f'the interface is {interface}')

def print_pkt(pkt):
    icmp_type=""
    if (pkt[ICMP].type==8):
        icmp_type="echo-request"
    elif (pkt[ICMP].type==0):
        icmp_type="echo-reply"
        
    print(f'Sniffed an {icmp_type} from {pkt[IP].src} to {pkt[IP].dst}')

pkt = sniff(iface=interface, filter='icmp', prn=print_pkt)
