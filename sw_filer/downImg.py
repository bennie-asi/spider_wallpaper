import requests, logging, time, os
from urllib.parse import *
from fake_useragent import UserAgent

# 日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(funcName)s -> %(message)s')


def Download_Image(
        downloadUrl: str or list, saveImagePath: str, headers: dict = None, proxies: dict = None
) -> bool or str:
    """
    1、下载图片

    :param downloadUrl: 下载的图片链接或者列表
    :param saveImagePath: 保存路径
    :param headers: 自定义头部信息
    :param proxies: 自定义代理
    :return:
    """

    agent = UserAgent()
    if isinstance(downloadUrl, str):
        downloadUrlParse = urlparse(downloadUrl)
        if headers is None:
            headers = {
                'User-Agent': agent.random,
                'Referer': f'{downloadUrlParse.scheme}://{downloadUrlParse.netloc}',
                'Host': downloadUrlParse.netloc,
            }

        # 下载
        try:
            response = requests.get(downloadUrl, headers=headers, timeout=20, proxies=proxies).content
        except TimeoutError:
            logging.info(f'下载图片超时：{downloadUrl}')
            return downloadUrl
        except Exception as e:
            logging.info(f'下载图片失败：{downloadUrl} -> 原因：{e}')
            return downloadUrl

        # 新保存路径
        if os.path.isdir(saveImagePath):
            newSaveImagePath = saveImagePath + r'\0.jpg'
        else:
            newSaveImagePath = os.path.splitext(saveImagePath)[0] + '.jpg'
        with open(newSaveImagePath, 'wb') as f:
            f.write(response)
            f.flush()

    elif isinstance(downloadUrl, list):
        # 循环下载
        for i in range(len(downloadUrl)):
            downloadUrlParse = urlparse(downloadUrl[i])
            if headers is None:
                headers = {
                    'User-Agent': agent.random,
                    'Referer': f'{downloadUrlParse.scheme}://{downloadUrlParse.netloc}',
                    'Host': downloadUrlParse.netloc,
                }
            if downloadUrl[i] == '':
                continue

            # 下载
            try:
                response = requests.get(downloadUrl[i], headers=headers, timeout=20, proxies=proxies).content
            except TimeoutError:
                logging.info(f'下载图片超时：{downloadUrl[i]}')
                return downloadUrl[i]
            except Exception as e:
                logging.info(f'下载图片失败：{downloadUrl[i]} -> 原因：{e}')
                continue

            # 新保存路径
            if os.path.isdir(saveImagePath):
                newSaveImagePath = saveImagePath + fr'\{i}.jpg'
            else:
                newSaveImagePath = os.path.splitext(saveImagePath)[0] + '.jpg'
            with open(newSaveImagePath, 'wb') as f:
                f.write(response)
                f.flush()

    else:
        logging.info('无法下载')
        return '无法下载'

    return True

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

if __name__ == '__main__':
    Download_Image(
        downloadUrl=['https://lmg.jj20.com/up/allimg/1114/121R0120545/20121Q20545-9-1200.jpg', 'https://lmg.jj20.com/up/allimg/1114/121R0120545/20121Q20545-10-1200.jpg'],
        saveImagePath=r'../target/'
    )

