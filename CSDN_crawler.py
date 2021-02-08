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

# 这是本人的 CSDN 个人博客主页，可以改成其他博主的
my_website = 'https://blog.csdn.net/qq_43413123'

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


# 爬取个人博客主页中博主的文章标题和文章链接
def get_url():
    urls = []
    page = 2
    for i in range(1, page+1):
        article_list = my_website + '/article/list/' + str(i)
        
        # 获取博客主页的网页内容
        soup = get_response(article_list)

        # 提取出网页中的文章列表内容
        #class="article-list"
        article_div = soup.find('div', attrs={'class': 'article-list'})

        # 提取出所有文章的信息
        articles_titles = article_div.find_all('h4')

        # 从每一条文章信息里面提取出文章的标题和链接信息
        articles = []
        for article_title in articles_titles:
            articles.append(article_title.find('a'))

        # 建立文章链接的集合，输出文章的标题和链接
        # 将每一篇文章的链接 url 加入文章链接集合中
        for article_url in articles:
            print(article_url.text.strip())
            urls.append(article_url.get("href"))
            print('URL : ', article_url.get("href"), end = '\n\n')

    #返回文章链接的集合
    return urls


# 爬取个人博客主页中关于博主的个人信息
def get_Profile():
    # 获取博客主页的网页内容
    soup = get_response(my_website)

    # 从网页内容中提取博主的个人简介信息
    #id="asideProfile"
    Profile = soup.find('div', attrs={'id': 'asideProfile'})

    # 提取关于（原创，粉丝...）的信息
    #class="data-info d-flex item-tiling"
    item_tiling = Profile.find('div', attrs={'class': 'data-info d-flex item-tiling'})
    # print(type(item_tiling))

    # 输出提取到的博主个人信息
    information = item_tiling.find_all('dl')
    for inf in information:
        # print(type(inf.text))
        classification = inf.find('dd')
        print(classification.text, end = " : ")
        print(inf.get('title'))

# 访问每一篇文章，获取文章的信息
def get_visit(url):
    # 获取文章的网页内容
    soup = get_response(url)

    # 提取文章的标题栏，得到文章的标题
    #class="article-title-box"
    article_title_box = soup.find('div', attrs={'class': 'article-title-box'})
    print('成功访问 : ', article_title_box.text.strip())

    # 提取文章的各种信息
    #class="article-bar-top"
    article_bar_top = soup.find('div', attrs={'class': 'article-bar-top'})

    # 提取文章的访问数
    # class="read-count"
    read_count = article_bar_top.find('span', attrs={'class': 'read-count'})
    print('访问：', read_count.text.strip(), end = '\t')

    # 提取文章的收藏数目
    # id="blog_detail_zk_collection"
    collection = article_bar_top.find('a', attrs={'id': 'blog_detail_zk_collection'})
    # class="get-collection"
    collection_num = collection.find('span', attrs={'class': 'get-collection'})

    # 使用正则表达式匹配收藏数的数值
    number = re.sub('\D', '', collection_num.text)
    print('收藏：', number, end='\n\n')

# main
if __name__ == '__main__':
    # 文章链接的集合
    all_urls = []

    # 爬取个人博客主页中关于博主的个人信息
    get_Profile()

    # 爬取个人博客主页中所有文章的信息，得到每篇文章的链接 url
    all_urls = get_url()
    print('获取到的链接数:',len(all_urls))

    # 查看爬取得到的文章链接 url
    for url in all_urls:
        print(url)

    # 访问每一篇文章，获取文章的信息（合法刷访问量）
    for loop in range(30):
        # 从文章链接集合中取出一条文章链接 url
        for url in  all_urls:
            try:
                # 访问这篇文章
                get_visit(url)

            except Exception as e:
                print(e)
                continue

        # 查看此时的博主个人博客信息
        get_Profile()

        # 等待一段时间
        sleep_time = random.randint(65, 80)
        print('等待', sleep_time, 's')
        time.sleep(sleep_time)