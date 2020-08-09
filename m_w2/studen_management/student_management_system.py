# 学生管理系统
# 1.初始化tcp服务端
# 2.处理客户端请求
import re

import gevent
import socket
from gevent import monkey

from studen_management.addr_analysis1 import recv_send

monkey.patch_all()


class HttpTcp(object):
    """学生管理系统服务端"""

    # 1.初始化tcp服务端
    def __init__(self):
        # 初始化
        self.tcp_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # 更新设置端口
        self.tcp_s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)

        # 绑定
        self.tcp_s.bind(('', 7077))

        # 设置监听
        self.tcp_s.listen(128)

    def accpet(self):
        # 2.1 循环处理客户端请求
        spawn_list = list()
        while True:
            client, addr = self.tcp_s.accept()

            # 2.2 多协程处理
            spawn_list.append(gevent.spawn(recv_send, client))


# #############################初始化tcp服务端完成############################################

def main():
    """学生管理系统服务端"""

    # 1.初始化tcp服务端
    stu_serve = HttpTcp()

    # 2.处理客户端请求
    stu_serve.accpet()


if __name__ == '__main__':
    main()
