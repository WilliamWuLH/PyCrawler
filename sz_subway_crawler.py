# 处理网页内容
from bs4 import BeautifulSoup
# 处理 url 资源
import requests
# 用于随机处理
import random
# 时间使用
import time
# 正则表达式使用
import re

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

# 这里的网站是深圳地铁线路的百度百科(1,2,3,4,5,7,9,11)
sz_1 = "https://baike.baidu.com/item/%E6%B7%B1%E5%9C%B3%E5%9C%B0%E9%93%811%E5%8F%B7%E7%BA%BF/6178769?fr=aladdin"
sz_2 = "https://baike.baidu.com/item/%E6%B7%B1%E5%9C%B3%E5%9C%B0%E9%93%812%E5%8F%B7%E7%BA%BF"
sz_3 = "https://baike.baidu.com/item/%E6%B7%B1%E5%9C%B3%E5%9C%B0%E9%93%813%E5%8F%B7%E7%BA%BF"
sz_4 = "https://baike.baidu.com/item/%E6%B7%B1%E5%9C%B3%E5%9C%B0%E9%93%814%E5%8F%B7%E7%BA%BF"
sz_5 = "https://baike.baidu.com/item/%E6%B7%B1%E5%9C%B3%E5%9C%B0%E9%93%815%E5%8F%B7%E7%BA%BF"
sz_7 = "https://baike.baidu.com/item/%E6%B7%B1%E5%9C%B3%E5%9C%B0%E9%93%817%E5%8F%B7%E7%BA%BF"
sz_9 = "https://baike.baidu.com/item/%E6%B7%B1%E5%9C%B3%E5%9C%B0%E9%93%819%E5%8F%B7%E7%BA%BF"
sz_11 = "https://baike.baidu.com/item/%E6%B7%B1%E5%9C%B3%E5%9C%B0%E9%93%8111%E5%8F%B7%E7%BA%BF"
res = ''

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

#爬取深圳地铁二号线的站点和一些其他线路（看网页的架构）
def get_2():
    ans = ''
    soup = get_response(sz_2)

    #class="body-wrapper"
    bodywrapper = soup.find('div', attrs={'class': 'body-wrapper'})

    #class="main-content"
    maincontent = bodywrapper.find('div', attrs={'class': 'main-content'})

    #log-set-param="table_view"
    tableview = maincontent.find('table', attrs={'log-set-param': 'table_view'})

    # 输出为建立字典的形式
    information = tableview.find_all('tr')
    for inf in information:
        # print(type(inf.text))
        #width="121"
        name = inf.find('td', attrs={'width': '121'})
        if name:
            # 每个站点后面都没有站，但是百度百科有站
            ans = ans + '\'' + name.text.replace(' ','').replace('站', '') + '\':'
        #width="69"
        index = inf.find('td', attrs={'width': '69'})
        if index:
            ans = ans + '\'02' + index.text.replace(' ','') + '\', '
    return ans

#爬取地铁三号线和一些其他线路（看网页的架构）
def get_3():
    ans = ''
    soup = get_response(sz_3)

    #class="body-wrapper"
    bodywrapper = soup.find('div', attrs={'class': 'body-wrapper'})

    #class="main-content"
    maincontent = bodywrapper.find('div', attrs={'class': 'main-content'})

    #log-set-param="table_view"
    tableview = maincontent.find('table', attrs={'log-set-param': 'table_view'})

    #输出为建立字典的形式
    information = tableview.find_all('tr')
    index = 1
    for inf in information:
        name = ''
        bb = inf.find_all('td')
        for ii in bb:
            tt = ii.find('a')
            # 每个站点后面都没有站，但是百度百科有站
            if tt and '站' in tt.text:
                ans = ans + '\'' + tt.text.replace(' ','').replace('站', '') + '\':'
                ans = ans + '\'03' + str(index) + '\', '
                index = index + 1
    return ans

#爬取地铁五号线和一些其他线路（看网页的架构）
def get_5():
    ans = ''
    soup = get_response(sz_5)
 
    #class="body-wrapper"
    bodywrapper = soup.find('div', attrs={'class': 'body-wrapper'})

    #class="main-content"
    maincontent = bodywrapper.find('div', attrs={'class': 'main-content'})

    #log-set-param="table_view"
    tableview = maincontent.find('table', attrs={'log-set-param': 'table_view'})

    #输出为建立字典的形式
    information = tableview.find_all('tr')
    index = 1
    for inf in information:
        name = ''
        bb = inf.find_all('td')
        for ii in bb:
            # 每个站点后面都没有站，但是百度百科有站
            if '站' in ii.text:
                ans = ans + '\'' + ii.text.replace(' ','').replace('站', '') + '\':'
                ans = ans + '\'05' + str(index) + '\', '
                index = index + 1
    return ans


# main
if __name__ == '__main__':
    # 爬取不同的地铁线路，仅需要更改线路的数字（其中有一些线路可以使用同一套函数爬取）
    res = 'subway3 = {'
    res = res + get_3()
    res = res + '}'
    print(res)
