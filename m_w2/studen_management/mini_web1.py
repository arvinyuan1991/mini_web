# mini_web

# 路由装饰器
url_dict = dict()


def route(url):
    def decorater(func):
        def wrapping(body_info):
            return func(body_info)

        url_dict[url] = wrapping
        return wrapping

    return decorater


# 获得响应信息
def dynamic(recv_addr, body_info):
    # print('连接上')
    respond_line = 'HTTP/1.1 200 OK\r\n'.encode('utf-8')

    try:
        print(url_dict)
        respond_body = url_dict[recv_addr](body_info).encode('utf-8')
    except Exception as e:
        respond_line = 'HTTP/1.1 404 NOT FOUND\r\n'.encode('utf-8')
        respond_body = '地址不存在！'.encode('utf-8')
    return respond_line, respond_body


# ###########################上面是框架，下面是代码#########################################


@route('/')
def login(body_info):
    """登陆界面"""
    with open('./student_login2.html', 'r') as f:
        new_content = ''
        while True:
            content = f.read(1024)
            if content:
                new_content += content
            else:
                return new_content
