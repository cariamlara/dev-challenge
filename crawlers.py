import requests
from bs4 import BeautifulSoup
import re
import json


class CrawlerTribunal():
    def __init__(self, sigla_tribunal):
        self.sigla_tribunal = sigla_tribunal

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
    
    def get_url(self):
        tribunal = self.sigla_tribunal
        num_processo = '0051575-54.2021.8.06.0071'
        placeholders = ['esaj', 'www2']
        if tribunal == 'tjce':
            base_url_1grau = f'https://{placeholders[0]}.{tribunal}.jus.br/cpopg/show.do?processo.codigo=&processo.foro={num_processo[-4:].lstrip("0")}&processo.numero={num_processo}'
            base_url_2grau = f'https://{placeholders[0]}.{tribunal}.jus.br/cposg5/search.do?conversationId=&paginaConsulta=0&cbPesquisa=NUMPROC&numeroDigitoAnoUnificado={num_processo[:15]}&foroNumeroUnificado={num_processo[-4:]}&dePesquisaNuUnificado={num_processo}&dePesquisaNuUnificado=UNIFICADO&dePesquisa=&tipoNuProcesso=UNIFICADO'
            return base_url_1grau, base_url_2grau
        else:
            base_url_1grau = f'https://{placeholders[1]}.{tribunal}.jus.br/cpopg/show.do?processo.codigo=&processo.foro=71&processo.numero='
            base_url_2grau = 'y'
            return base_url_1grau, base_url_2grau


    def get_num(self, num):
        pass


    def get_1grau(self, num):
        base_url_1grau, base_url_2grau = self.get_url()
        num_processo = num
        url_1grau = base_url_1grau + num_processo
        print(url_1grau)
        try:
            response = requests.get(url_1grau)
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
            pretty = json.dumps(self.results, indent=4)
            print(pretty)
            # return self.results

        except:
            raise
    
    def check_2grau(self):
        response = requests.get(url)
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


    def collect_lawsuit(self, num):
        num_processo = num
        self.get_1grau(num_processo)
        self.get_2grau(num_processo)
        pretty = json.dumps(self.results, indent=4)
        print(pretty)
    
court_name = 'tjce'
crawler_tjce = CrawlerTribunal('tjce')
crawler_tjce.get_1grau('0051575-54.2021.8.06.0071')
#crawler_tjce.collect_lawsuit()