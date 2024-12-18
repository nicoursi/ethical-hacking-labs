# Task 2.B: Protecting the Internal Network
# In this task, we will set up firewall rules on the router to protect the internal network 192.168.60.0/24.
# More specifically, we need to enforce the following restrictions on the ICMP traffic:

# 1. Outside hosts cannot ping internal hosts.
# 2. Outside hosts can ping the router.
# 3. Internal hosts can ping outside hosts.
# 4. All other packets between the internal and external networks should be blocked

# You can find out the interface names via the ip addr command

# 1. Outside hosts cannot ping internal hosts.

# In the case of 192.168.60.0/24 the internal interface is eth01:
# 98: eth1@if99: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default
#     link/ether 02:42:c0:a8:3c:0b brd ff:ff:ff:ff:ff:ff link-netnsid 0
#     inet 192.168.60.11/24 brd 192.168.60.255 scope global eth1
#        valid_lft forever preferred_lft forever

iptables -v -A FORWARD -p icmp --icmp-type echo-request -o eth1 -j DROP
# iptables -v -A FORWARD -p icmp --icmp-type echo-reply -i eth1 -j ACCEPT

# 2. Outside hosts can ping the router.
iptables -v -A INPUT -p icmp --icmp-type echo-request -j ACCEPT
iptables -v -A OUTPUT -p icmp --icmp-type echo-reply -j ACCEPT

# 3. Internal hosts can ping outside hosts.
iptables -v -A FORWARD -p icmp --icmp-type echo-request -i eth1 -o !eth1 -j ACCEPT
iptables -v -A FORWARD -p icmp --icmp-type echo-reply -i !eth1 -o eth1 -j ACCEPT

# 4. All other packets between the internal and external networks should be blocked
iptables -v -P FORWARD DROP
