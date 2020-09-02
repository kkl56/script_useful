'''需要用到的模块：sshtunnel,paramiko
通过sshtunnel建立客户端与跳板机的隧道，然后再通过paramiko链接服务器即可
常见配置如下：
'''
import paramiko

from sshtunnel import SSHTunnelForwarder


def ssh_forward(jumpIp, jumpPort, jumpUser, jumpPass, serverIp, serverPort, serverUser, serverPass, command):
    localIp = '127.0.0.1'
    localPort = 998
    with SSHTunnelForwarder ((jumpIp, jumpPort),
        ssh_username = jumpUser,
        #ssh_pkey='/home/username/.ssh/xx',
        ssh_password = jumpPass,
        remote_bind_address = (serverIp, serverPort),
        local_bind_address=(localIp, localPort)) as server:
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(server.local_bind_host, server.local_bind_port, username = serverUser, password = serverPass)
        stdin, stdout, stderr = client.exec_command(command)
        print(stdout.read().decode('utf-8'))
        client.close( )

if __name__ == '__main__':
    args=['192.168.180.132',22,'root','123',   '192.168.180.55',22,'root','123456',  'df ']
    ssh_forward(args[0],args[1],args[2],args[3],args[4],args[5],args[6],args[7],args[8])
    #ssh_forward("192.168.180.132",22,"root","123","192.168.180.55",22,"root","123456",'ls')
'''
port1，port2为服务器开放端口，localPort是自己定义的端口

参考：https://github.com/pahaz/sshtunnel
'''
