import docker
import sys

client = docker.from_env()
containers = []


def cm_start(num, images=['alpine', 'ubuntu', 'busybox', 'debian']):
    assert len(images) != 0
    for i in range(num):
        temp = client.containers.create(images[i % len(images)], "sh", tty=True)
        containers.append(temp)
    print("Containers created .. ")
    for container in containers:
        print(container)
    cm_print_status()
    # start containers
    for container in containers:
        container.start()
    cm_print_status()
    cm_save()


def cm_print_status():
    for i in range(len(containers)):
        print("Container", i, " status .. ", containers[i].status)


def cm_exec(num, command):
    for i in range(num):
        a, b = containers[i % len(containers)].exec_run(command, tty=True)
        print(b)


def cm_save():
    file = open("containers.txt", "w")
    for container in containers:
        file.write(container.id + '\n')
    file.close()


def cm_stop(keep=False, time=0):
    for container in containers:
        container.stop(timeout=time)
    if not keep:
        client.containers.prune()


if __name__ == '__main__':
    argc = len(sys.argv)
    assert argc >= 2
    match sys.argv[1]:
        case "create":
            print("A")
        case "start":
            print("A")
        case "exec":
            print("A")
        case "stop":
            print("A")
        case "copy":
            print("A")