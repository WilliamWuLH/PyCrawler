# 处理网页内容
from bs4 import BeautifulSoup
# 处理 url 资源
import requests
# 用于随机处理
import random

# user_agent库：每次执行一次访问随机选取一个 user_agent，防止过于频繁访问被禁止
USER_AGENT_LIST = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]

# 输入 url，请求网页并且输出网页信息
def get_response(url):
    # random.choice 从 user_agent 库中随机取出 user_agent 构建请求头
    headers = {
        'user-agent':random.choice(USER_AGENT_LIST)
    }
    # GET
    resp = requests.get(url,headers=headers)
    # 判断是否出现异常
    resp.raise_for_status()
    # 使用 lxml 解析器
    soup = BeautifulSoup(resp.content, 'lxml')
    
    return soup

# 
def get_information(url):
    out_information = []
    # 
    soup = get_response(url)

    # 
    #id="component_59"
    component = soup.find('ul', attrs={'id': 'component_59'})

    # 
    information = component.find_all('li')

    for i in information:
        book_information = []
        # print(i)
        temp = i.find_all('p')
        for t in temp:
            # print(t.text)
            book_information.append(t.text)
        out_information.append(book_information)
    return out_information

# main
if __name__ == '__main__':
    # 当当网上关于“数据挖掘”与“数据分析”的图书信息的 URL
    dangdang = 'http://search.dangdang.com/?key=%CA%FD%BE%DD%CD%DA%BE%F2&act=input'

    # 
    out_inf = get_information(dangdang)

    for i in out_inf:
        # print('信息数目：', len(i))
        print('书名：',i[1])
        print('描述：',i[2])
        print('价格：',i[3])
        print('评论数目：',i[4])
        print('作者，出版时间，出版社：',i[5])