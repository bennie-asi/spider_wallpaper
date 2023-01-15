def main():
    import time
    from sw_wallpaper.base import get_wallpaper_urls
    from sw_filer.downFile import start
    base_url = 'https://wallhaven.cc/toplist'
    for page in range(1, 100):
        print(time.strftime("%H:%M:%S"))
        print("第{}页".format(page))
        url = (base_url+'?page={}').format(page)
        wallpaper_urls = get_wallpaper_urls(url)
        for wallpaper_url in wallpaper_urls:
            start(wallpaper_url, save_path=r'C:\Users\18203\Pictures\Camera Roll')


if __name__ == "__main__":
    main()
