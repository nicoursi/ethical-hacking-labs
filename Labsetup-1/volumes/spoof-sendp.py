#!/usr/bin/env python3
from scapy.all import *
from search_iface_by_prefx import *
  
interface = search_iface_by_prefx("br-", get_if_list())

ip = IP()
ip.src = '10.9.0.6'
ip.dst = '10.9.0.5'

icmp = ICMP()
packet = Ether()/ip/icmp
packet.show()

sendp(packet, iface=interface)
