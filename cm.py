# Python Version 3.10
import docker
import sys


def cm_create(num, images=['ubuntu'], volume=''):
    """
    Create containers without starting them.
    :param volume: The volume you want to mount to the container.
    :param num: The number of containers you want to create.
    :param images: A list of images of containers.
    """
    assert len(images) != 0
    if volume != '':
        try:
            volume = client.volumes.get(volume)
            mp = docker.types.Mount("/home", volume)
        except docker.errors.NotFound:
            print("The volume does not exist.")
            return
        except docker.errors.APIError:
            print("The server returns an error.")
            return
    for i in range(num):
        try:
            if volume != '':
                temp = client.containers.create(images[i % len(images)], "sh", tty=True, mounts=[mp], name=str(i))
            else:
                temp = client.containers.create(images[i % len(images)], "sh", tty=True)
        except docker.errors.ImageNotFound:
            print("The specified image does not exist.")
            cm_stop()
            return
        except docker.errors.APIError:
            print("The server returns an error.")
            cm_stop()
            return
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


def cm_create_volume(name):
    """
    Create a volume and return.
    :param name: Name of the volume.
    """
    try:
        volume = client.volumes.create(name=name, driver='local',
                                       driver_opts={'foo': 'bar', 'baz': 'false'},
                                       labels={"key": "value"})
    except docker.errors.APIError:
        print("The server returns an error.")
        return
    return volume


client = docker.from_env()
containers = client.containers.list(True)
cm_save()

if __name__ == '__main__':
    argc = len(sys.argv)
    assert argc >= 2
    match sys.argv[1]:
        case "create":
            if len(sys.argv) == 3:
                cm_create(int(sys.argv[2]))
            elif len(sys.argv) == 4:
                cm_create(int(sys.argv[2]), list(sys.argv[3]))
            elif len(sys.argv) == 5:
                cm_create(int(sys.argv[2]), list(sys.argv[3]), sys.argv[4])
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
        case "createVolume":
            cm_create_volume(sys.argv[2])
