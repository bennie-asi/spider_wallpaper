import os
import time
from urllib.parse import unquote

import requests


def get_file_name(url, headers):
    filename = ''
    if 'Content-Disposition' in headers and headers['Content-Disposition']:
        disposition_split = headers['Content-Disposition'].split(';')
        if len(disposition_split) > 1:
            if disposition_split[1].strip().lower().startswith('filename='):
                file_name = disposition_split[1].split('=')
                if len(file_name) > 1:
                    filename = unquote(file_name[1])
    if not filename and os.path.basename(url):
        filename = os.path.basename(url).split("?")[0]
    if not filename:
        return time.time()
    return filename


def download_file(response, file_name, save_path):
    print('正在写入文件%s' % file_name)
    with open(save_path + file_name, "wb") as pyFile:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                pyFile.write(chunk)
        pyFile.flush()
    print("文件%s已保存" % file_name)


def start(url, headers=None, save_path=r'../target/', stream=True, allow_redirects=False, timeout=5):

    if not headers:
        from fake_useragent import UserAgent
        headers = {'User-Agent': UserAgent().random, 'Connection': 'close'}
    while True:
        try:
            print('尝试从%s下载中' % url)
            get_file = requests.get(url=url, headers=headers, stream=stream, allow_redirects=allow_redirects, timeout=timeout)
            break
        except requests.exceptions.ConnectionError:
            print('下载文件连接出错，正在重试')
        except requests.exceptions.ReadTimeout:
            print('下载文件读取超时，正在重试')
    try:
        content_length = get_file.headers['Content-Length']  # Transfer-Encoding:chunked时为块传输，无content_length
    except KeyError:
        content_length = '未获取到'
        print('Transfer-Encoding:chunked时为块传输，无content_length')
    response = get_file
    file_name = get_file_name(url, get_file.headers)
    download_file(response, file_name, save_path)
    print("文件大小：", content_length, "文件名称：" + file_name)


if __name__ == '__main__':
    file_path = '../target/'
    url = 'https://iterm2.com/downloads/stable/iTerm2-3_3_6.zip'
    headers = {
    }
    # start(url, save_path=file_path, headers=headers)
