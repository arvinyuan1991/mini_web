import re

from pymysql import connect

url_dict = dict()
def route(url):
    """"""
    def decorater(func):
        def wrapping(recv_data):

            return func(recv_data)

        url_dict[url] = wrapping
        return wrapping
    return decorater


def addr_logic(addr_data,recv_data):
    """根据不同的地址返回不同响应体"""
    respond_line = 'HTTP/1.1 200 OK\r\n'.encode('utf-8')
    print(url_dict)
    try:
        respond_body_info = url_dict[addr_data](recv_data)
        # print(respond_body_info)
        respond_body = respond_body_info.encode('utf-8')
    except Exception as e:
        respond_line = 'HTTP/1.1 404 NOT FOUND\r\n'.encode('utf-8')
        respond_body = '地址不存在！'.encode('utf-8')

    return respond_line,respond_body

##############################上面是框架，下面是代码##########################################
@route('/home.html')
def home(recv_data):
    return '回家'

@route('/login.html')
def login(recv_data):
    # print('login执行')
    with open('./student_login.html','r') as f:
        # print('正在读')
        content = f.read()

    return content
@route('/student_regit.html')
def login(recv_data):
    # print('login执行')
    with open('./student_regit.html','r') as f:
        # print('正在读')
        content = f.read()

    return content

@route('/mp4.html')
def mp4(recv_data):
    with open('./mp4.html') as f:
        content = f.read()
    return content


@route('/index.html')
def index(recv_data):
    """股票信息"""
    # 1.获取前端数据
    with open('./templates/index.html','r') as f:
        content = f.read()

    # 2.从数据库得到数据
    conn = connect(host='127.0.0.1',port=3306,user='root',password='mysql',database='stock_db',charset='utf8')
    cs = conn.cursor()

    cs.execute('select * from info;')

    data = cs.fetchall()

    cs.close()
    conn.close()

    # 3.拼接
    row_str = """
    	<tr>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>
                <input type="button" value="添加" id="toAdd" name="toAdd" systemidvaule="%s">
            </td>
            </tr>
    	"""
    table_str = ''
    for tmp in data:
        table_str += row_str%(tmp[0],tmp[1],tmp[2],tmp[3],tmp[4],tmp[5],tmp[6],tmp[7],tmp[1])

    new_content = re.sub("\{%content%\}", table_str, content)

    return new_content


@route('/center.html')
def index(recv_data):
    """股票信息"""
    # 1.获取前端数据
    with open('./templates/center.html', 'r') as f:
        content = f.read()

    # 2.从数据库得到数据
    conn = connect(host='127.0.0.1', port=3306, user='root', password='mysql', database='stock_db', charset='utf8')
    cs = conn.cursor()

    cs.execute('select info.code,info.short,info.chg,info.turnover,info.price,info.highs,focus.note_info from info inner join focus on focus.info_id = info.id;')

    data = cs.fetchall()

    cs.close()
    conn.close()

    # 3.拼接
    # 定义一行的字符串
    row_str = """<tr>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>
                    <a type="button" class="btn btn-default btn-xs" href="/update/%s.html"> <span class="glyphicon glyphicon-star" aria-hidden="true"></span> 修改 </a>
                </td>
                <td>
                    <input type="button" value="删除" id="toDel" name="toDel" systemidvaule="%s">
                </td>
            </tr>"""
    table_str = ''
    for tmp in data:
        table_str += row_str % (tmp[0], tmp[1], tmp[2], tmp[3], tmp[4], tmp[5], tmp[6], tmp[0], tmp[0])

    new_content = re.sub("\{%content%\}", table_str, content)

    return new_content







