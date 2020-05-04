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

def get_response(url):
    headers = {
        'user-agent':random.choice(USER_AGENT_LIST),
    }

    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.content, 'lxml')
    return soup

def get_charts_hero(soup):
    #id="charts"
    charts = soup.find('div', attrs={'id': 'charts'})

    #class="charts-hero"
    charts_hero = charts.find('div', attrs={'class', 'charts-hero'})
    print('\nChart : ', charts_hero.text.strip(), end='\n\n')

    #class="date-selector__button button--link"
    date = charts.find('button', attrs={'class', 'date-selector__button button--link'})
    print('Date : ', date.text.strip(), end='\n\n')


def get_chart_list(soup):
    #class="chart-list container"
    chart_list = soup.find('div', attrs={'class', 'chart-list container'})

    #class="chart-list__elements"
    elements = chart_list.find_all('li')

    for element in elements:
        #class="chart-element__rank__number"
        rank = element.find('span', attrs={'class', 'chart-element__rank__number'})
        print(rank.text, end='\t')

        #class="chart-element__information__song text--truncate color--primary"
        song = element.find('span', attrs={'class', 'chart-element__information__song text--truncate color--primary'})
        print('Song : ', song.text)

        #class="chart-element__information__artist text--truncate color--secondary"
        artist = element.find('span', attrs={'class', 'chart-element__information__artist text--truncate color--secondary'})
        print('Artist : ', artist.text)

        #class="chart-element__meta text--center color--secondary text--last"
        LAST_WEEK = element.find('span', attrs={'class', 'chart-element__meta text--center color--secondary text--last'})
        print('LAST WEEK : ', LAST_WEEK.text, end='\t\t')

        #class="chart-element__meta text--center color--secondary text--peak"
        PEAK = element.find('span', attrs={'class', 'chart-element__meta text--center color--secondary text--peak'})
        print('PEAK : ', PEAK.text, end='\t')

        #class="chart-element__meta text--center color--secondary text--week"
        DURATION = element.find('span', attrs={'class', 'chart-element__meta text--center color--secondary text--week'})
        print('DURATION : ', DURATION.text)

        print()

if __name__ == "__main__":
    url = [ 'https://www.billboard.com/charts/hot-100',
            'https://www.billboard.com/charts/billboard-200']
    soup = get_response(url[0])
    get_charts_hero(soup)
    get_chart_list(soup)

    #TODO  弄个 class 来存榜单的歌曲信息