import requests
from bs4 import BeautifulSoup
import vk
import os

path_ = os.getcwd() + '//' 

def get_version():
    r = requests.get('https://vk.com/dev/versions').text
    site = BeautifulSoup(r, features = 'lxml')
    element = site.find(class_="dev_version_num fl_l")
    v = element.get_text()
    
    return v

def download_video_vk(url, filename):
    #
    #Загружает видео из вк принимая ссылку на плеер
    #
    r = requests.get(url).text
    site = BeautifulSoup(r, features = 'lxml')
    try:
        element = str( site.find_all('source')[1] ) ### 0 = 1 questionmark
    except:
        print('Видеозапись была помечена модераторами сайта как «Материал для взрослых»')
        return ''
    str1 = element.find('\"')+1
    str2 = element[str1:].find('\"') + str1
    url = element[str1:str2]
    r = requests.get(url)
    f = r.content

    with open(path_ + filename + '.mp4', 'wb') as file:
        file.write(f)

v = get_version()

if __name__ == '__main__':
    download_video_vk('https://cs573204.vkuservideo.net/10/efcPjIxMjg-MjM/videos/ef06815817.720.mp4', 'file')