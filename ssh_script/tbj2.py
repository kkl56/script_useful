"""
需要用到的模块：sshtunnel,paramiko
通过sshtunnel建立客户端与跳板机的隧道，然后再通过paramiko链接服务器即可
常见配置如下:
"""
import paramiko
from sshtunnel import SSHTunnelForwarder
with SSHTunnelForwarder (
    ('192.168.180.132',22),
    ssh_username='root',
    # ssh_pkey='/home/username/.ssh/xx',
    ssh_password='123',
    remote_bind_address=('192.168.180.55', 22),
    local_bind_address=('127.0.0.1', 22)
) as server:
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect('127.0.0.1', 22, 'root',"123456")
    stdin, stdout, stderr = client.exec_command('ls')
    print(stdout.read())
    client.close()
"""
port1，port2为服务器开放端口，port3是自己定义的端口

参考：https://github.com/pahaz/sshtunnel
"""