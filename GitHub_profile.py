from bs4 import BeautifulSoup
import requests
import random

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

URLs = [
    "https://github.com/WilliamWuLH",
    "https://github.com/leelitian",
    "https://github.com/KimbingNg",
    "https://github.com/JameyWoo",
    "https://github.com/CynricFeng",
    "https://github.com/YalandHong",
    "https://github.com/YihaoChan",
    "https://github.com/sillywutong",
    "https://github.com/wangzhebufangqi"
]

def get_response(url):
    headers = {
        'user-agent':random.choice(USER_AGENT_LIST),
    }

    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.content, 'lxml')
    return soup

def get_profile():
    soup = get_response(URLs[0])
    # print(soup)

    #class="vcard-names-container float-left col-9 col-md-12 pt-1 pt-md-3 pb-1 pb-md-3 js-sticky js-user-profile-sticky-fields"
    name = soup.find('div', attrs={'class': 'vcard-names-container float-left col-9 col-md-12 pt-1 pt-md-3 pb-1 pb-md-3 js-sticky js-user-profile-sticky-fields'})
    print(name.text.strip())

    #class="UnderlineNav width-full user-profile-nav js-sticky top-0"
    nav = soup.find('div', attrs={'class': 'UnderlineNav width-full user-profile-nav js-sticky top-0'})
    print(nav.text.strip().replace(' ','').replace('\n', ' '))

    #class="js-calendar-graph mx-3 d-flex flex-column flex-items-end flex-xl-items-center overflow-hidden pt-1 is-graph-loading graph-canvas calendar-graph height-full text-center"
    contributions = soup.find('div', attrs={'class': 'js-calendar-graph mx-3 d-flex flex-column flex-items-end flex-xl-items-center overflow-hidden pt-1 is-graph-loading graph-canvas calendar-graph height-full text-center'})
    everyday = contributions.find_all('rect')
    sum = 0
    month_sum = 0
    pre_month = 0
    for day in everyday:
        #data-count="0"
        count = day.get("data-count")
        #data-date="2020-04-17"
        date = day.get("data-date")
        # print(date)
        if count != "0":
            month = (date.split('-'))[1]
            if pre_month != month:
                print(pre_month, " : ", month_sum)
                month_sum = 0
            print(date, " : ", count)
            sum += int(count)
            month_sum += int(count)
            pre_month = month
    print(pre_month, " : ", month_sum)
    print("sum : ", sum)


if __name__ == "__main__":
    get_profile()