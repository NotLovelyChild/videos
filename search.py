from bs4 import BeautifulSoup
import requests
from video_model import *
from urllib.parse import urlparse
import config

class zuida_search():
    def __init__(self, key):
        self.key = key
        self.main_url = 'http://www.zuidazy4.com'
        self.search_url = self.main_url + '/index.php?m=vod-search&submit=search&wd='
        self.video_info = video_info()
        self.series_info = series_info()

    def start_search(self):
        result = []
        self.search_url += self.key
        re = requests.post(self.search_url)
        soup = BeautifulSoup(re.text, 'html.parser')
        list = soup.find_all(name='span', attrs={'class': 'xing_vb4'})
        for li in list:
            href = self.main_url + li.find('a')['href']
            result.append({'title': li.text, 'href': href})

        return result

    def get_item_detail(self, item_url):
        information = ''
        soup = config.requestUrl(item_url)
        title_div = soup.find(name='div', attrs={'class': 'vodh'})
        title = title_div.find('h2').text
        series = title_div.find('span').text
        score = title_div.find('label').text
        infos = soup.find(name='div', attrs={'class': 'vodinfobox'}).find_all('li')
        self.video_info.title = title
        self.video_info.series = series
        self.video_info.score = score

        for li in infos:
            information += ('\n%s' % li.text)
        self.video_info.information = information

        box = soup.find_all(name='div', attrs={'class':'ibox playBox'})
        videos_m3u8 = []
        videos_mp4 = []
        videos_online = []
        for b in box:
            videos = b.find_all('li')
            for video in videos:
                series = series_info()
                video_info = video.text.split('$')
                video_title = video_info[0]
                video_href = video_info[-1]
                series.title = video_title
                series.href = video_href
                if '.m3u8' in video_href:
                    videos_m3u8.append(series)
                elif '.mp4' in video_href:
                    videos_mp4.append(series)
                else:
                    videos_online.append(series)

        self.video_info.videos_m3u8 = videos_m3u8
        self.video_info.videos_mp4 = videos_mp4
        self.video_info.videos_online = videos_online

        return self.video_info

    def parsing_m3u8(self, url):
        host = '%s://%s' % (urlparse(url).scheme, urlparse(url).hostname)
        soup = config.requestUrl(url)
        js_group = soup.find_all(name='script', attrs={'type': 'text/javascript'})
        for js in js_group:
            js_str = str(js)
            for row in js_str.split('var'):
                if '.m3u8' in row:
                    video_url = host + row.replace('main = "','').replace('";','').replace(' ','')
                    print(video_url)

