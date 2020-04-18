from bs4 import BeautifulSoup
import requests
import random
import time

#uer_agent库，随机选取，防止被禁
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

my_website = 'https://blog.csdn.net/qq_43413123'

#请求网页的代码整合
def get_response(url):
    #random.choice从一个集合中随机选出请求头
    headers = {
        'user-agent':random.choice(USER_AGENT_LIST)
    }

    resp = requests.get(url,headers=headers)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.content, 'lxml')
    return soup


def get_url():
    soup = get_response(my_website)

    #class="article-list"
    article_div = soup.find('div', attrs={'class': 'article-list'})
    articles_titles = article_div.find_all('h4')

    articles = []
    for article_title in articles_titles:
        articles.append(article_title.find('a'))

    urls = []
    for article_url in articles:
        urls.append(article_url.get("href"))
        print(article_url.text)
        print('URL : ', article_url.get("href"))

    return urls

def get_Profile():
    soup = get_response(my_website)

    #id="asideProfile"
    Profile = soup.find('div', attrs={'id': 'asideProfile'})

    #class="data-info d-flex item-tiling"
    item_tiling = Profile.find('div', attrs={'class': 'data-info d-flex item-tiling'})
    print(type(item_tiling))

    information = item_tiling.find_all('dl')
    for inf in information:
        # print(type(inf.text))
        print(inf.text.strip())

def get_visit(url):
    soup = get_response(url)

    #class="article-title-box"
    article_title_box = soup.find('div', attrs={'class': 'article-title-box'})
    print('成功访问 : ', article_title_box.text.strip())

    #class="article-bar-top"
    article_bar_top = soup.find('div', attrs={'class': 'article-bar-top'})

    # class="read-count"
    read_count = article_bar_top.find('span', attrs={'class': 'read-count'})

    print(read_count.text.strip(), end='\n\n')

if __name__ == '__main__':
    all_urls = []
    get_Profile()
    all_urls = get_url()
    print('获取到的链接数:',len(all_urls))

    for loop in range(10):
        for url in  all_urls:
            try:
                get_visit(url)

            except Exception as e:
                print(e)
                continue
        #wait
        sleep_time = random.randint(65, 80)
        print('等待', sleep_time, 's')
        time.sleep(sleep_time)