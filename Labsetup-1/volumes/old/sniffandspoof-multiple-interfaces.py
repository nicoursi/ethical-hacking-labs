#!/usr/bin/env python3
from scapy.all import *

def search_iface_by_prefx(search_string, string_list):
    matches = [item for item in string_list if search_string in item]
    return matches[0]
    
interfaces = get_if_list() #we will sniff on any interface in order reply to pings to externat networks
print (f'the interface is {search_iface_by_prefx("br-", interfaces)}')
interface = search_iface_by_prefx("br-", interfaces)
mac_address = get_if_hwaddr(interface)
print(f'This machine mac address is: {mac_address}')

def handle_sniffing(pkt):
    if ARP in pkt and pkt[ARP].op == 1:  # ARP request
        #if pkt[ARP].pdst in ip_range:
        print ("an ARP request arrived!")
        pkt.show()   
        
        arp_reply = ARP(op=2, hwsrc=mac_address, psrc=pkt[ARP].pdst,hwdst=pkt[ARP].hwsrc, pdst=pkt[ARP].psrc)
        send(arp_reply, verbose=False)
        #send(arp_reply, iface=interface, verbose=True)
             
        print(f"Sent ARP reply for {pkt[ARP].pdst}")
        arp_reply.show()
    else: # ICMP request
        print ("an ICMP request arrived!")
        pkt.show()
        icmp_reply = ICMP(type=0, id=pkt[ICMP].id, seq=pkt[ICMP].seq)
        ip_reply = IP(src=pkt[IP].dst, dst=pkt[IP].src)
        fullreply = ip_reply/icmp_reply/pkt[Raw]
        send(fullreply, verbose=False)
        print ("ICMP reply sent!")
        fullreply.show()

pkt = sniff(iface=interfaces, filter='arp[6:2] = 1 or icmp[icmptype] = 8', prn=handle_sniffing)
