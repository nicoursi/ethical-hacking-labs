#!/usr/bin/env python3
from scapy.all import *

destination = '142.250.184.206'
ttl = 1
ping_id = 100
i = 1
prev_replier = None
while True:
    ip = IP(dst=destination, ttl=ttl)
    ping = ICMP(id=ping_id)
    packet = ip/ping
    rsp = sr1(packet, timeout=1, verbose=0)
    if rsp is not None:
        replier = rsp.getlayer(IP).src 
        if replier!=prev_replier and rsp[ICMP].type==11 and rsp[ICMP].code==0:
            print (f'Hop {i}: {replier} ')
            prev_replier = replier
            i += 1
        elif rsp[ICMP].type==0:
            print(f'The destination ({replier}) has been reached! TTL={ttl}')
            break
    ttl += 1
    ping_id += 1
    

