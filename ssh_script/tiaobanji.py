import paramiko
from sshtunnel import SSHTunnelForwarder


class Jump_Server():
    def login_server(self, address, address_port, username, remote_address, remote_address_port, **kw):
        """
        :param address:       跳扳机的IP地址
        :param address_port:  跳扳机的端口号
        :param username:      跳板机的SSH登录账号
        :param remote_address:      远程服务器的IP地址
        :param remote_address_port: 远程服务器的端口号
        :param kw: 参数ssh_pkey(客户端私钥路径)参数key_password(客户端开机密码) 参数ssh_password(客户端密码)
        :return:  返回服务器操作指针
        """
        try:
            # 通过密钥调用connect函数建立Linux连接
            if "ssh_pkey" in kw.keys():
                server = SSHTunnelForwarder(
                    # 跳板机ip与ssh登录端口号
                    ssh_address_or_host=(address, address_port),
                    # 跳板机登录账号
                    ssh_username=username,
                    # PC(客户端)的私钥路径
                    ssh_pkey=paramiko.RSAKey.from_private_key_file(kw["ssh_pkey"]),
                    # PC(客户端)的密码
                    ssh_private_key_password=kw["key_password"],
                    # 远程MYSQL服务器的绑定的IP和端口号
                    remote_bind_address=(remote_address, remote_address_port)
                )
            # 通过密码调用connect函数建立Linux连接
            elif "password" in kw.keys():
                server = SSHTunnelForwarder(
                    ssh_address_or_host=(address, address_port),
                    ssh_username=username,
                    ssh_password=kw["password"],
                    remote_bind_address=(remote_address, remote_address_port),
                    # 绑定本地地址(默认127.0.0.1和端口号)及与跳板机相通的端口
                    local_bind_address=('127.0.0.1', 22),
                )
            else:
                print("登录信息与方法错误，抛出异常 - ValueError")
                raise ValueError
            server.start()
            print("账号【%s】登录【%s】服务器启动服务器【%s】的MySQL服务" % (username, address, remote_address))
            return server
        except Exception as e:
            print("发生未知错误: %s" % e)
            raise

    def logout_server(self, server_pointer):
        """
        :param server_pointer: 服务器操作指针
        :return:
        """
        try:
            server_pointer.close()
            print("登出服务器成功")
        except Exception as e:
            print("发生未知错误: %s" % e)
            raise