---
author:
- Nicola Ursino
date: 'October 30, 2024'
title: Ethical Hacking - Firewall Exploration Lab
numbersections: false
geometry: margin=2.5cm
output:
  pdf_document:
    pandoc_args: "--highlight-style=tango"
---

# Task 2.A: Protecting the Router

## Allow only ICMP requests and replies

``` bash
iptables -v -A INPUT -p icmp --icmp-type echo-request -j ACCEPT
iptables -v -A OUTPUT -p icmp --icmp-type echo-reply -j ACCEPT
iptables -v -P OUTPUT DROP # Set default rule for OUTPUT
iptables -v -P INPUT DROP # Set default rule for INPUT
```
## Questions
1. Can you ping the router?

Yes

2. Can you telnet into the router (a telnet server is running on all the containers?

No it is blocked

## Clean up
``` bash
iptables -v -F
iptables -v -P OUTPUT ACCEPT
iptables -v -P INPUT ACCEPT
```

## Or restart the container
``` bash
docker restart <Container ID>
```

# Task 2.B: Protecting the Internal Network
In this task, we will set up firewall rules on the router to protect the internal network **192.168.60.0/24**.
More specifically, we need to enforce the following restrictions on the ICMP traffic:

2. Outside hosts cannot ping internal hosts.
1. Outside hosts can ping the router.
3. Internal hosts can ping outside hosts.
4. All other packets between the internal and external networks should be blocked

You can find out the interface names via the `ip addr` command

## 1. Outside hosts cannot ping internal hosts.

In the case of **192.168.60.0/24** the internal interface is eth01:

``` bash
98: eth1@if99: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default
    link/ether 02:42:c0:a8:3c:0b brd ff:ff:ff:ff:ff:ff link-netnsid 0
    inet 192.168.60.11/24 brd 192.168.60.255 scope global eth1
       valid_lft forever preferred_lft forever
```
``` bash
iptables -v -A FORWARD -p icmp --icmp-type echo-request -o eth1 -j DROP
iptables -v -A FORWARD -p icmp --icmp-type echo-reply -i eth1 -j ACCEPT
```

## 2. Outside hosts can ping the router.
``` bash
iptables -v -A INPUT -p icmp --icmp-type echo-request -j ACCEPT
iptables -v -A OUTPUT -p icmp --icmp-type echo-reply -j ACCEPT
```

## 3. Internal hosts can ping outside hosts.
``` bash
iptables -v -A FORWARD -p icmp --icmp-type echo-request -i eth1 ! -o eth1 -j ACCEPT
iptables -v -A FORWARD -p icmp --icmp-type echo-reply ! -i eth1 -o eth1 -j ACCEPT
```

## 4. All other packets between the internal and external networks should be blocked
``` bash
iptables -v -P FORWARD DROP
```

# Task 2.C: Protecting Internal Server

In this task, we want to protect the TCP servers inside the internal network (192.168.60.0/24). More
specifically, we would like to achieve the following objectives where all the internal hosts run a
telnet server (listening to port 23):

1. Outside hosts can only access the  telnet server on 192.168.60.5, not the other internal hosts.
2. Outside hosts cannot access other internal servers.
3. Internal hosts can access all the internal servers.
4. Internal hosts cannot access external servers.
5. In this task, the connection tracking mechanism is not allowed. It will be used in a later task.

# 1. Outside hosts can only access the  telnet server on 192.168.60.5, not the other internal hosts.
``` bash
iptables -v -A FORWARD ! -d 192.168.60.5 -p tcp --dport 23 ! -i eth1 -j DROP
```

# 2. Outside hosts cannot access other internal servers.
Already accomplished by command 1

# 3. Internal hosts can access all the internal servers.
Already accomplished by command 1

# 4. Internal hosts cannot access external servers.

``` bash
iptables -v -A FORWARD -p tcp --dport 23 ! -o eth1 -j DROP
```

# 5. In this task, the connection tracking mechanism is not allowed. It will be used in a later task.
