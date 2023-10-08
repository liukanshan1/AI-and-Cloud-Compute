# AI-and-Cloud-Compute
### 麦吉尔大学暑期PBL交流课程人工智能与云计算Project

>>> python3 cm.py create 3
This command will create three docker containers with Ubuntu operating system.
>>> python3 cm.py create 3 centos
This command will create three docker containers with Centos operating system.
>>> python3 cm.py start
This command will start all docker containers.
>>> python3 cm.py exec “ls”
This command will make all docker containers execute “ls” command.
>>> pyhton3 cm.py exec 2 “ls”
This command will make two docker containers execute “ls” command.
>>> python3 cm.py stop
This command will stop all docker containers immediately.
>>> python3 cm.py stop 3
This command will wait three seconds and stop all docker containers.
>>> python3 cm.py list
This command will list all docker containers.
The cluster manager is able to create any number docker containers and start executing some commands in these docker containers.
