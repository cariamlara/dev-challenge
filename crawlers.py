import requests
from bs4 import BeautifulSoup
import re
import json


class CrawlerTribunal():
    def __init__(self, nome, url):
        self.nome = nome
        self.url = url

    paths = [
            'classeProcesso',
            'assuntoProcesso',
            'areaProcesso',
            'juizProcesso',
            'dataHoraDistribuicaoProcesso',
            'valorAcaoProcesso',
            'tablePartesPrincipais'
            ]
    
    results = { '1grau' : {},
               '2grau': {},}
    
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

            resultados = {} 

            for path in self.paths:
                element = soup.find('span', attrs={'id': path}) or soup.find('div', attrs={'id': path}) or soup.find('table', attrs={'id': path})
                if element:
                    resultados[path] = str(element.text.replace("\n", "").replace("\t", "").replace("\xa0", ""))
                else:
                    resultados[path] = 'nao consta'
            
            self.results['1grau'] = resultados
            # retty = json.dumps(self.results, indent=4)
            return self.results

        except:
            raise
    
    def check_2grau(self):
        response = requests.get('https://esaj.tjce.jus.br/cposg5/search.do?conversationId=&paginaConsulta=0&cbPesquisa=NUMPROC&numeroDigitoAnoUnificado=0051575-54.2021&foroNumeroUnificado=0071&dePesquisaNuUnificado=0051575-54.2021.8.06.0071&dePesquisaNuUnificado=UNIFICADO&dePesquisa=&tipoNuProcesso=UNIFICADO')
        content = response.content
        soup = BeautifulSoup(content, 'html.parser')
        alert = soup.find('td', attrs={'role' : 'alert'})
        if alert:
            should_get_2grau = False
            self.results['2grau'] = 'Esse processo não tem 2 grau'
            return should_get_2grau, content
            """
            alert_text = alert.text
            print(alert_text)
            """
        else:
            should_get_2grau = True
            return should_get_2grau, content
            """
            print('nao tem alerta, liberado pra crawlear')
            xiripingo = soup.find('div', attrs={'id' : 'classeProcesso'}).text
            print(xiripingo)
            """

    def get_2grau(self):
        should_get_2grau, content = self.check_2grau()
        if should_get_2grau == True:
            soup = BeautifulSoup(content, 'html.parser')
            resultados2 = {} 

            for path in self.paths:
                element = soup.find('span', attrs={'id': path}) or soup.find('div', attrs={'id': path}) or soup.find('table', attrs={'id': path})
                if element:
                    resultados2[path] = str(element.text.replace("\n", "").replace("\t", "").replace("\xa0", ""))
                else:
                    resultados2[path] = 'nao consta'
            
            self.results['2grau'] = resultados2
            
            # pretty = json.dumps(self.results, indent=4)
            return self.results
        else:
            return


    def collect_lawsuit(self):
        self.get_1grau('0051575-54.2021.8.06.0071')
        self.get_2grau()
        pretty = json.dumps(self.results, indent=4)
        print(pretty)
    

crawler_tjce = CrawlerTribunal('tjce', 'https://esaj.tjce.jus.br/cpopg/show.do?processo.codigo=1Z0000ET90000&processo.foro=71&processo.numero=')
crawler_tjce.collect_lawsuit()