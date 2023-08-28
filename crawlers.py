import requests
from bs4 import BeautifulSoup
import re

class CrawlerTribunal():
    def __init__(self, nome, url):
        self.nome = nome
        self.url = url


    def get_url(self, num):
        base_url = self.url
        url = f'{base_url}'
        num_processo = num
        new_url = url + num
        try:
            response = requests.get(new_url)
            content = response.content
            soup = BeautifulSoup(content, 'html.parser')
            num_processo_el = soup.find('span', attrs={'id' : 'varaProcesso'})
            num_processo = num_processo_el.text
            print(num_processo)
        except:
            raise

    def collect_lawsuits():
        return
    
    def save_as_json():
        return

   
crawler_tjal = CrawlerTribunal('tjal', "https://www2.tjal.jus.br/cpopg/show.do?processo.codigo=[0-9A-Z]{12}&processo.foro=1&processo.numero=")
crawler_tjal.get_url("0001019-40.2012.8.02.0050")
