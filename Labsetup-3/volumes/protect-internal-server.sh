#In this task, we want to protect the TCP servers inside the internal network (192.168.60.0/24). More
#specifically, we would like to achieve the following objectives.

# All the internal hosts run a telnet server (listening to port 23).

# 1. Outside hosts can only access the  telnet server on 192.168.60.5, not the other internal hosts.

# 2. Outside hosts cannot access other internal servers.

# 3. Internal hosts can access all the internal servers.

# 4. Internal hosts cannot access external servers.

# 5. In this task, the connection tracking mechanism is not allowed. It will be used in a later task.
