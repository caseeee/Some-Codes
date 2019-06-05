import requests
from bs4 import BeautifulSoup
from retrying import retry
import re
import os


headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36',
        'Referer': 'https://music.163.com/',
    }

@retry(wait_random_min=1000, wait_random_max=2000)
def get_html(url):
    """获取页面内容"""
    try:
        req = requests.get(url, headers, timeout=5)
        html = req.content
        soup = BeautifulSoup(html, 'html.parser')
        return soup
    except ConnectionError:
        print("请求超时")

def get_song():
    """获取歌单"""

    # 获取歌单链接特征
    url = "https://music.163.com/discover"
    all_the_list = get_html(url).findAll('a', {'class': 'msk', 'data-res-action': 'log'})   # 筛选出来的结果为歌单和电台
    song_list = []
    for i in all_the_list:
        song = i.get('href')    # 获取href的内容
        contain = '/playlist?' in song  # 包含'/playlist?'
        # 判断是否为'/playlist?'来区分歌单和电台
        if contain is True:
            song_list.append(song)  # 把歌单添加到songs列表中
        else:
            continue

    # 通过歌单页面来获取歌曲并且下载
    for j in song_list:
        url = "https://music.163.com" + j
        # 获取歌单名称
        song_list_name = get_html(url).find('title').string
        #　创建歌单目录
        try:
            os.mkdir("./" + song_list_name)
        except FileExistsError or FileNotFoundError:
            continue
        songs = get_html(url).findAll('a', {"href": re.compile(r"\/song\?id=\d+?")})
        for k in songs:
            song_name = k.string  # 获取歌曲的名字
            song_id = k.get("href")
            download_url = "http://music.163.com/song/media/outer/url?id=" + song_id[9:] + ".mp3"
            print("下载的歌曲为:  " + song_name + '\n')
            # 获取下载的内容
            download_songs = requests.get(download_url, headers=headers).content
            try:
                with open('./' + song_list_name + "/" + song_name + '.mp3', 'wb') as file:
                    file.write(download_songs)
            except FileExistsError or FileNotFoundError:
                continue

    print('Done!')


if __name__ == '__main__':
    get_song()