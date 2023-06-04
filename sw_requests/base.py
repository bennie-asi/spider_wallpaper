import requests
from bs4 import BeautifulSoup


def request(url, timeout=5):
    '''传入一个url，返回一个通过lxml解析的bs4对象'''
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.76'

    headers = {'User-Agent': user_agent, 'Connection': 'close'}
    print("正在请求%s中" % url)
    while True:
        try:
            response = requests.get(url, headers=headers, timeout=timeout)
            break
        except requests.exceptions.ConnectionError:
            print('请求出错了，正在重试')
        except requests.exceptions.ReadTimeout:
            print('请求读取超时，正在重试')
    print('response已取得')
    if response.status_code == 404 or response.status_code == 429:
        print('请求失败~', response.status_code)
    response.encoding = response.apparent_encoding
    soup = BeautifulSoup(response.text, 'lxml')
    return soup


if __name__ == "__main__":
    url = 'https://wallhaven.cc/toplist'
    soup = request(url)
    # print(soup)
    figures = soup.find_all('figure')
    nexturl = soup.find(attrs={'class': 'next'})['href']
    # print(nexturl)
    print(figures)
    #
    # print(soup.find('figure').find('a')['href'])



