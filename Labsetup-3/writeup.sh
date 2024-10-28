
# Task 2.A: Protecting the Router

## allow only icmp requests and replies
```
iptables -A INPUT -p icmp --icmp-type echo-request -j ACCEPT
iptables -A OUTPUT -p icmp --icmp-type echo-reply -j ACCEPT
iptables -P OUTPUT DROP # Set default rule for OUTPUT
iptables -P INPUT DROP # Set default rule for INPUT
```
## Questions
1. Can you ping the router?
Yes

2. Can you telnet into the router (a telnet server is running on all the containers?
No it is blocked

## clean up
```
iptables -F
iptables -P OUTPUT ACCEPT
iptables -P INPUT ACCEPT
```

## or restart the container
```
docker restart <Container ID>
```

# Task 2.B: Protecting the Internal Network
In this task, we will set up firewall rules on the router to protect the internal network **192.168.60.0/24**.
More specifically, we need to enforce the following restrictions on the ICMP traffic:

1. Outside hosts cannot ping internal hosts.
2. Outside hosts can ping the router.
3. Internal hosts can ping outside hosts.
4. All other packets between the internal and external networks should be blocked

You can find out the interface names via the `ip addr` command

## 1. Outside hosts cannot ping internal hosts.

In the case of **192.168.60.0/24** the internal interface is eth01:
```
98: eth1@if99: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default
    link/ether 02:42:c0:a8:3c:0b brd ff:ff:ff:ff:ff:ff link-netnsid 0
    inet 192.168.60.11/24 brd 192.168.60.255 scope global eth1
       valid_lft forever preferred_lft forever
```
```
iptables -A FORWARD -p icmp --icmp-type echo-request -o eth1 -j DROP
# iptables -A FORWARD -p icmp --icmp-type echo-reply -i eth1 -j ACCEPT
```

## 2. Outside hosts can ping the router.
```
iptables -A INPUT -p icmp --icmp-type echo-request -j ACCEPT
iptables -A OUTPUT -p icmp --icmp-type echo-reply -j ACCEPT
```

## 3. Internal hosts can ping outside hosts.
```
iptables -A FORWARD -p icmp --icmp-type echo-request -i eth1 -o !eth1 -j ACCEPT
iptables -A FORWARD -p icmp --icmp-type echo-reply -i !eth1 -o eth1 -j ACCEPT
```

## 4. All other packets between the internal and external networks should be blocked
```
iptables -P FORWARD DROP
```
