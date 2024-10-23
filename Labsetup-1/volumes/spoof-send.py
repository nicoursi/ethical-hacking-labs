#!/usr/bin/env python3
from scapy.all import *

ip = IP(dst = '10.9.0.5', src = '10.9.0.6' )
icmp = ICMP()
packet = ip/icmp
packet.show()

send(packet)

