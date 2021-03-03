import requests
from bs4 import BeautifulSoup
import json
import random
import time

from requests.api import get

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

def get_response(url):
    # random.choice 从 user_agent 库中随机取出 user_agent 构建请求头
    headers = {
        'user-agent':random.choice(USER_AGENT_LIST)
    }
    # GET
    r = requests.get(url,headers=headers)
    # 判断是否出现异常
    r.raise_for_status()
    r.encoding = 'utf-8'
    return r

if __name__ == "__main__":
    # 
    the_urls = [
        'http://hdjw.hnu.edu.cn/resService/data/ignore/language/zh_CN/document/XSMH0902.json?t=1614354390523',
        'http://hdjw.hnu.edu.cn/resService/data/ignore/language/zh_CN/document/XSMH0901.json?t=1614354390522',
        'http://hdjw.hnu.edu.cn/resService/data/ignore/language/zh_CN/document/XSMH09.json?t=1614354390523',
    ]

    # 
    data1 = json.loads(get_response(the_urls[0]).text)
    for k, v in data1['data'].items():
        print('{} : {}'.format(k, v))
    
    # 
    data2 = json.loads(get_response(the_urls[1]).text)
    for k, v in data2['data'].items():
        print('{} : {}'.format(k, v))
