# Python Version 3.10
import docker
import sys
import time


def cm_create(num, images=['alpine', 'ubuntu', 'busybox', 'debian']):
    """
    Create containers without starting them.
    :param num: The number of containers you want to create.
    :param images: A list of images of containers.
    """
    assert len(images) != 0
    for i in range(num):
        try:
            temp = client.containers.create(images[i % len(images)], "sh", tty=True)
        except docker.errors.ImageNotFound:
            print("The specified image does not exist.")
            cm_stop()
        except docker.errors.APIError:
            print("The server returns an error.")
            cm_stop()
        else:
            containers.append(temp)
            print("Container created .. " + temp.id)
    cm_print_status()
    cm_save()


def cm_start():
    """
    Start all containers.
    """
    for container in containers:
        container.start()
    cm_print_status()
    cm_save()


def cm_print_status():
    """
    Print containers status.
    """
    containers = client.containers.list(True)
    for i in range(len(containers)):
        print("Container", i, containers[i].id, " status:", containers[i].status)


def cm_exec(num, command):
    """
    Run a command inside containers.
    :param num: The number of containers you want to run the command.
    :param command: Command to be executed.
    """
    for i in range(num):
        try:
            exitCode, output = containers[i % len(containers)].exec_run(command, tty=True)
        except docker.errors.APIError:
            print("The No.", i, " server returns an error.")
        else:
            print(str(output, "utf-8"))
    cm_save()


def cm_save():
    """
    Save container status in a file.
    """
    containers = client.containers.list(True)
    file = open("containers.txt", "w")
    for container in containers:
        file.write(container.id + " " + container.status + '\n')
    file.write('\n')
    file.close()


def cm_stop(time=0):
    """
    Stop containers.
    :param time: Timeout in seconds to wait for the container to stop before sending a SIGKILL.
    """
    for container in containers:
        container.stop(timeout=time)
    cm_print_status()
    cm_save()


def cm_delete():
    """
    Delete containers.
    """
    client.containers.prune()
    cm_print_status()
    cm_save()


client = docker.from_env()
containers = client.containers.list(True)
cm_save()


if __name__ == '__main__':
    argc = len(sys.argv)
    assert argc >= 2
    match sys.argv[1]:
        case "create":
            cm_create(int(sys.argv[2]))
        case "start":
            cm_start()
        case "exec":
            if len(sys.argv) == 3:
                cm_exec(len(containers), sys.argv[2])
            elif len(sys.argv) == 4:
                cm_exec(int(sys.argv[2]), sys.argv[3])
        case "stop":
            if len(sys.argv) == 2:
                cm_stop()
            elif len(sys.argv) == 3:
                cm_stop(int(sys.argv[2]))
        case "delete":
            cm_delete()
        case "list":
            cm_print_status()
