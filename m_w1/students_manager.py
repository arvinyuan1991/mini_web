# 服务器多任务协程版
# 1,tcp初始化
# 2,处理客户端请求
import re

import gevent
import socket
from gevent import monkey
from pymysql import connect

monkey.patch_all()
from day17.mini_web import addr_logic


class Http_tcp(object):
    """http的tcp服务端初始化"""

    def __init__(self):
        # 1.socket初始化
        # 2.重新绑定端口设置
        # 3.绑定端口
        # 4.监听设置

        # 1.socket初始化
        self.tcp_sever = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # 2.重新绑定端口设置
        self.tcp_sever.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)

        # 3.绑定端口
        self.tcp_sever.bind(('', 8088))

        # 4.监听设置
        self.tcp_sever.listen(128)

    def accpet(self):
        """循环处理客户请求协程版"""
        spawn_list = list()
        while True:
            client, addr = self.tcp_sever.accept()
            spawn_list.append(gevent.spawn(self.handle, client))

        gevent.joinall(spawn_list)

    def handle(self, client):
        """根据不同的请求地址分析对应的响应"""
        respond_line = 'HTTP/1.1 200 OK\r\n'.encode('utf-8')
        respond_head = 'content-type:text/html;charset=utf-8;\r\n'.encode('utf-8')
        respond_empty = '\r\n'.encode('utf-8')
        recv_info = client.recv(1024)
        if recv_info:
            recv_data = recv_info.decode('utf-8')
            # print(recv_data)
            addr_match = re.match('[^ ]+ ([^ ]+) ', recv_data)
            # print(addr_match)
            if addr_match:
                addr_data = addr_match.group(1)
                print(addr_data)
                # 结尾是.html的地址
                if addr_data.endswith('.html'):
                    respond_line, respond_body = addr_logic(addr_data,recv_data)

                else:
                    # 打开图片或视频
                    if addr_data.startswith('/images'):
                        # print('图片打开')
                        with open('.' + addr_data, 'rb') as f:
                            respond_body = b''
                            while True:
                                content = f.read(1024)
                                if content:
                                    respond_body += content
                                else:
                                    break
                    # 学生注册
                    elif addr_data.endswith('regit.mysql'):
                        # 获取请求体的内容
                        recv_body = re.search('name.+', recv_data).group()
                        # print(recv_body)
                        students_list = re.split('=|&', recv_body)
                        if len(students_list) == 8:

                            r_name = students_list[1]
                            r_password = students_list[3]
                            r_age = students_list[5]
                            r_gender = students_list[7]

                            # 连接数据库进行数据更新
                            conn = connect(host='127.0.0.1', port=3306, user='root', password='mysql', database='p23',
                                           charset='utf8')
                            cs = conn.cursor()
                            print(type(r_name))

                            cs.execute(
                                """insert into students(name,password,age,gender) values('%s','%s',%s,%s);""" % (
                                    r_name, r_password, r_age, r_gender))

                            # data = cs.fetchall()
                            conn.commit()

                            cs.close()
                            conn.close()

                            # 成功界面
                            with open('./successful.html', 'rb') as f:
                                # print('正在读')
                                content = f.read()


                            respond_body = content

                        else:
                            # 注册失败界面
                            with open('./fail_regit.html', 'rb') as f:
                                # print('正在读')
                                content = f.read()

                            respond_body = content


                    # 登陆系统
                    elif addr_data.endswith('student_login.mysql'):
                        # 获取请求体的内容
                        recv_body = re.search('name.+', recv_data).group()
                        print(recv_body)
                        students_list = re.split('=|&', recv_body)
                        r_name = students_list[1]
                        r_password = students_list[3]
                        print(r_name, r_password)

                        # 2.从数据库得到数据
                        conn = connect(host='127.0.0.1', port=3306, user='root', password='mysql', database='p23',
                                       charset='utf8')
                        cs = conn.cursor()

                        cs.execute('select * from students;')

                        data = cs.fetchall()

                        cs.close()
                        conn.close()

                        for tmp in data:
                            print(tmp)
                            if tmp[1] == r_name:
                                if tmp[2] == r_password:
                                    with open('./mp4.html', 'rb') as f:
                                        respond_body = b''
                                        while True:
                                            content = f.read(1024)
                                            if content:
                                                respond_body += content
                                            else:
                                                break
                                    break
                        else:
                            # 登陆失败界面
                            with open('./fail.html', 'rb') as f:
                                # print('正在读')
                                content = f.read()

                            respond_body = content

                    # 打开前端
                    else:
                        try:
                            respond_head = b''
                            # print('正在打开')
                            with open('./static%s' % addr_data, 'rb') as f:
                                # print('打开成功')
                                respond_body = b''
                                while True:
                                    content = f.read(1024)
                                    if content:
                                        respond_body += content

                                    else:
                                        # print(respond_body)
                                        # print('读取成功')
                                        break
                        except Exception as e:
                            respond_line = 'HTTP/1.1 404 NOT FOUND\r\n'.encode('utf-8')
                            respond_body = '地址不存在！'.encode('utf-8')
            else:
                respond_line = 'HTTP/1.1 404 NOT FOUND\r\n'.encode('utf-8')
                respond_body = '地址不存在！'.encode('utf-8')
        else:
            respond_line = 'HTTP/1.1 404 NOT FOUND\r\n'.encode('utf-8')
            respond_body = '地址不存在！'.encode('utf-8')

        send_info = respond_line + respond_head + respond_empty + respond_body
        # print(send_info)
        client.send(send_info)
        client.close()


def main():
    """服务器多任务协程版"""

    # 1,tcp初始化
    tcp_init = Http_tcp()
    # 2,处理客户端请求
    tcp_init.accpet()


if __name__ == '__main__':
    main()
