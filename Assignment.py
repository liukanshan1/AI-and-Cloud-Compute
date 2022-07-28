# Python Version 3.10
import docker
import sys

client = docker.from_env()
containers = client.containers.list(True)


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
    for i in range(len(containers)):
        print("Container", i, " status ", containers[i].status)


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
            print(str(output,"utf-8"))
    cm_save()


def cm_save():
    """
    Save container status in a file.
    """
    file = open("containers.txt", "w")
    for container in containers:
        file.write(container.id + " " + container.status + '\n')
    file.write('\n')
    file.close()


def cm_stop(keep=False, time=0):
    """
    Stop containers and delete them if you want.
    :param keep: True if you want to keep stopped containers.
    :param time: Timeout in seconds to wait for the container to stop before sending a SIGKILL.
    """
    for container in containers:
        container.stop(timeout=time)
    if not keep:
        client.containers.prune()
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
            cm_exec(int(sys.argv[2]), sys.argv[3])
        case "stop":
            cm_stop()
