import paramiko
from sshtunnel import SSHTunnelForwarder
import threading


def readData(shell):
    while True:
        data = shell.recv(2048)
        if not data:
            print("quit now")
            break
        data = data.decode()
        print(data, end = "")


def main():
    port104 = 22
    port105 = 22
    localport = 995
    with SSHTunnelForwarder(ssh_address_or_host=('192.168.180.132', 22), ssh_username="root", ssh_password="123",
                            remote_bind_address=("192.168.180.55", 22), local_bind_address=('127.0.0.1', localport)) as tunnel:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(tunnel.local_bind_host, tunnel.local_bind_port, username = "root", password = "123456")
        shell = client.invoke_shell()

        thread = threading.Thread(target=readData, args=(shell,))
        thread.start()

        shell.sendall("pwd\n")
        shell.sendall("ifconfig\n")
        shell.sendall("exit\n")

        thread.join()
        client.close()


if __name__ == '__main__':
    main()