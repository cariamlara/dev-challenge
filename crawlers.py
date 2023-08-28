import requests
from bs4 import BeautifulSoup
import re
import json

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
            paths = [
                    'varaProcesso',
                    'classeProcesso',
                    'assuntoProcesso',
                    'areaProcesso',
                    'juizProcesso',
                    'dataHoraDistribuicaoProcesso',
                    'valorAcaoProcesso',
                    'tablePartesPrincipais'
                    ]
            
            resultados = {} 

            for path in paths:
                element = soup.find('span', attrs={'id': path}) or soup.find('div', attrs={'id': path}) or soup.find('table', attrs={'id': path})
                if element:
                    resultados[path] = str(element.text.replace("\n", "").replace("\t", "").replace("\xa0", ""))
                else:
                    resultados[path] = 'nao consta'
            
            pretty = json.dumps(resultados, indent=4)
            print(pretty)

        except:
            raise

    def collect_lawsuits():
        return
    
    def save_as_json():
        return

   
crawler_tjal = CrawlerTribunal('tjal', "https://www2.tjal.jus.br/cpopg/show.do?processo.codigo=[0-9A-Z]{12}&processo.foro=1&processo.numero=")
crawler_tjal.get_url("0001557-39.2012.8.02.0044")
