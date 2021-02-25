import os
import ffmpy3
import requests
from bs4 import BeautifulSoup
from multiprocessing.dummy import Pool as ThreadPool

search_keyword = '旺达幻视'
search_url = 'https://www.okzyw.net/index.php'
search_params = {
    'm' : 'vod-search'
}
search_headers = {
    'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36',
    'referer' : 'https://www.okzyw.net/',
    'origin' : 'https://www.okzyw.net',
    'host' : 'www.okzyw.net',
}
search_datas = {
    'wd' : search_keyword,
    'submit' : 'search',
}

video_path = 'F:/video/'
video_dir = ''

r = requests.post(url=search_url, params=search_params, headers=search_headers, data=search_datas)
r.encoding = 'utf-8'
server = 'https://www.okzyw.net'
search_html = BeautifulSoup(r.text, 'lxml')
search_spans = search_html.find_all('span', class_='xing_vb4')
for span in search_spans:
    url = server + span.a.get('href')
    name = span.a.string
    print(url)
    print(name)
    video_dir = name
    if video_dir not in os.listdir(video_path):
        os.mkdir(video_path + video_dir)
    
    detail_url = url
    r = requests.get(url = detail_url)
    r.encoding = 'utf-8'
    detail_bf = BeautifulSoup(r.text, 'lxml')
    num = 1
    search_res = {}
    for each_url in detail_bf.find_all('input'):
        if 'm3u8' in each_url.get('value'):
            url = each_url.get('value')
            if url not in search_res.keys():
                search_res[url] = num
            print('第%03d集 : ' % num)
            print(url)
            num += 1

def downloadVideo(url):
    num = search_res[url]
    name = os.path.join(video_path + video_dir, '第%03d集.mp4' % num)
    ffmpy3.FFmpeg(inputs={url:None}, outputs={name:None}).run()

pool = ThreadPool(8)
results = pool.map(downloadVideo, search_res.keys())
pool.close()
pool.join()