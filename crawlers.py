import requests
from bs4 import BeautifulSoup
import re
import json


class CrawlerTribunal():
    def __init__(self, nome, url):
        self.nome = nome
        self.url = url

    def get_num(self, num):
        pass


    def get_1grau(self, num):
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
            return pretty

        except:
            raise
    
    def check_2grau(self):
        response = requests.get('https://esaj.tjce.jus.br/cposg5/search.do?conversationId=&paginaConsulta=0&cbPesquisa=NUMPROC&numeroDigitoAnoUnificado=8500269-87.2023&foroNumeroUnificado=0035&dePesquisaNuUnificado=8500269-87.2023.8.06.0035&dePesquisaNuUnificado=UNIFICADO&dePesquisa=&tipoNuProcesso=UNIFICADO')
        content = response.content
        soup = BeautifulSoup(content, 'html.parser')
        alert = soup.find('td', attrs={'role' : 'alert'})
        if alert:
            alert_text = alert.text
            print(alert_text)
        else:
            print('nao tem alerta, liberado pra crawlear')
            xiripingo = soup.find('div', attrs={'id' : 'classeProcesso'}).text
            print(xiripingo)

    def get_2grau(self):
        pass

    def collect_lawsuit():
        pass
    
crawler_tjce = CrawlerTribunal('tjce', 'https://tjce.com.br')
crawler_tjce.check_2grau()