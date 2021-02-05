from bs4 import BeautifulSoup
import requests


class zuida_search():
    def __init__(self, key):
        self.key = key
        self.main_url = 'http://www.zuidazy4.com'
        self.search_url = self.main_url + '/index.php?m=vod-search&submit=search&wd='

    def start_search(self):
        self.search_url += self.key
        re = requests.post(self.search_url)
        soup = BeautifulSoup(re.text, 'html.parser')
        list = soup.select('.xing_vb4')
        for li in list:
            print(li.text)
            a = li.select('a')
            if len(a):
                href = self.main_url + a[0]['href']
                print(href)
