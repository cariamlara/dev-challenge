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
            vara_processo = (soup.find('span', attrs={'id' : 'varaProcesso'})).text
            classe = (soup.find('span', attrs={'id' : 'classeProcesso'})).text
            assunto = (soup.find('span', attrs={'id' : 'assuntoProcesso'})).text
            area = (soup.find('div', attrs={'id' : 'areaProcesso'})).text
            juiz = (soup.find('span', attrs={'id' : 'juizProcesso'})).text
            data_distribuicao = (soup.find('div', attrs={'id' : 'dataHoraDistribuicaoProcesso'})).text
            valor_acao = (soup.find('div', attrs={'id' : 'valorAcaoProcesso'})).text
            partes_processo = (soup.find('table', attrs={'id' : 'tablePartesPrincipais'})).text

            infos = { "numero_processo" : num, 
                     "vara_processo" : vara_processo,
                     "classe_processo" : classe,
                     "assunto_processo" : assunto,
                     "area_processo" : area,
                     "juiz_processo": juiz,
                     "data_distribuicao" : data_distribuicao,
                     "valor_acao" : valor_acao,
                     "partes_processo" : partes_processo,
                     }

            print(infos)
        except:
            raise

    def collect_lawsuits():
        return
    
    def save_as_json():
        return

   
crawler_tjal = CrawlerTribunal('tjal', "https://www2.tjal.jus.br/cpopg/show.do?processo.codigo=[0-9A-Z]{12}&processo.foro=1&processo.numero=")
crawler_tjal.get_url("0001019-40.2012.8.02.0050")
