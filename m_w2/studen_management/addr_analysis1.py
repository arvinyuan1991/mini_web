import re
from studen_management.mini_web1 import dynamic


def recv_send(client):
    """根据接收的地址分析响应"""

    # 3.1 默认响应行，响应头，空行设置
    respond_line = 'HTTP/1.1 200 OK\r\n'.encode('utf-8')
    respond_head = 'Content-type:text/html;charset=utf-8;\r\n'.encode('utf-8')
    respond_empty = '\r\n'.encode('utf-8')

    # 地址分析异常处理
    try:
        # 3.2 接收信息
        recv_info = client.recv(1024 * 1024)

        recv_data = recv_info.decode('utf-8')

        # 3.3 获取地址
        match_addr_info = re.match('[^ ]+ ([^ ]+) ', recv_data)

        # 3.4 分析地址

        recv_addr = match_addr_info.group(1)

        print(recv_addr)
        # 3.5 动态资源处理
        if recv_addr.endswith('.html') or recv_addr == '/':
            # print('成功')

            # 3.51 响应体信息解析成字典
            body_info = recv_data.split('\r\n')[1]
            # body_list = body_info.split('&')
            # info_dict = dict()
            # for info in body_list:
            #     info_list = info.split('=')
            #     info_dict[info_list[0]] = info_list[1]

            respond_line, respond_body = dynamic(recv_addr, body_info)

        # 3.6 静态资源处理
        else:
            with open('recv_data', 'rb') as f:
                respond_head = b''
                respond_body = b''
                while True:
                    content = f.read(1024)
                    if content:
                        respond_body += content
                    else:
                        break

    # 捕获异常
    except Exception as r:
        respond_line = 'HTTP/1.1 404 NOT FOUND\r\n'.encode('utf-8')
        respond_body = '地址不存在！'.encode('utf-8')

    send_info = respond_line + respond_head + respond_empty + respond_body
    client.send(send_info)
    client.close()
