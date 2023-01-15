import random
import time

from sw_filer.downFile import start
from sw_requests.base import request


def get_wallpaper_urls(url):
    """传入一个url将其下所有的壁纸详情url返回"""
    res = list()
    soup = request(url)
    # next_url = soup.find(attrs={'class': 'next'})['href']  # 下一页url
    figures = soup.find_all('figure')
    for figure in figures:
        b = random.randint(1, 2)  # 随机从1到2内取一个整数值
        print("等待" + str(b) + "秒")
        time.sleep(b)  # 把随机取出的整数值传到等待函数中
        url = figure.find('a')['href']
        print("获取图片地址中~")
        url = get_img_url(url)
        print("已捕获到图片URL：%s" % url)
        # Download_Image(downloadUrl=url, saveImagePath=r'../target/')
        # start(url=url)
        res.append(url)
    return res


def get_img_url(url):
    """传入壁纸详情url返回壁纸的url"""
    soup = request(url)
    wallpaper = soup.find(id='wallpaper')
    return wallpaper['src']


if __name__ == "__main__":
    url = 'https://wallhaven.cc/toplist?page=1'
    urls = get_wallpaper_urls(url)

    print(urls)
    # Download_Image(downloadUrl=urls, saveImagePath=r'../target/')
