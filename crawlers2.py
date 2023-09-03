import requests
from bs4 import BeautifulSoup
import re
import json
 

class CrawlerTribunal():
    def __init__(self, sigla_tribunal):
        self.sigla_tribunal = sigla_tribunal
        self.results = {'1grau': {}, 
                        '2grau': {}}

    paths = [
            'classeProcesso',
            'assuntoProcesso',
            'areaProcesso',
            'juizProcesso',
            'dataHoraDistribuicaoProcesso',
            'valorAcaoProcesso',
            'tablePartesPrincipais'
            ]
    
    def extract_info_1grau(self, url):
        response = requests.get(url)
        content = response.content
        soup = BeautifulSoup(content, 'html.parser')
        check_if_exists = soup.find('span', attrs={'id' : 'numeroProcesso'})
        
        resultados = {} 
        
        if check_if_exists:
            for path in self.paths:
                element = soup.find('span', attrs={'id': path}) or soup.find('div', attrs={'id': path}) or soup.find('table', attrs={'id': path})
                if element:
                    resultados[path] = str(element.text.replace("\n", "").replace("\t", "").replace("\xa0", ""))
                else:
                    resultados[path] = 'Não consta'
                    
            self.results['1grau'] = resultados
            pretty = json.dumps(self.results, indent=4)
            return pretty
            # return self.results

    def extract_info_2grau(self, url):
        response = requests.get(url)
        content = response.content
        soup = BeautifulSoup(content, 'html.parser')
        check_if_exists = soup.find('span', attrs={'id' : 'numeroProcesso'})
        
        resultados = {} 

        if check_if_exists:
            for path in self.paths:
                element = soup.find('span', attrs={'id': path}) or soup.find('div', attrs={'id': path}) or soup.find('table', attrs={'id': path})
                if element:
                    resultados[path] = str(element.text.replace("\n", "").replace("\t", "").replace("\xa0", ""))
                else:
                    resultados[path] = 'Não consta'

            self.results['2grau'] = resultados
            pretty = json.dumps(self.results, indent=4)
            return pretty
            # return self.results
        else:
            return
                



    def get_1grau(self, num_processo):
        num = num_processo  # esse número de processo eu vou tirar do JSON, jogar na funcao de coletar os dados e todas as outras funções vão herdar
        # num = '0007750-06.1992.8.02.0001'  # tjal
        # num = '0051575-54.2021.8.06.0071' # tjce
        name = self.sigla_tribunal
        if name == 'tjal':  # nome criado junto com a classe, precisa herdar esse nome praqui pra dentro
            url_1grau = f'https://www2.tjal.jus.br/cpopg/show.do?processo.codigo=&processo.foro={num[-4:].lstrip("0")}&processo.numero={num}'
           # return url_1grau
        else:
            url_1grau = f'https://esaj.tjce.jus.br/cpopg/show.do?processo.codigo=&processo.foro={num[-4:].lstrip("0")}&processo.numero={num}'
            # return url_1grau
        
        infos = self.extract_info_1grau(url_1grau)
        print(infos)


    def check_2grau(self, url):
        response = requests.get(url)
        content = response.content
        soup = BeautifulSoup(content, 'html.parser')
        alert = soup.find('td', attrs={'role' : 'alert'})
        password_modal = soup.find('td', attrs={'class' : 'modalTitulo'})
        if alert:
            should_get_2grau = False
            self.results['2grau'] = 'Esse processo não tem 2 grau.'
            return should_get_2grau
            """
            alert_text = alert.text
            print(alert_text)
            """
        elif password_modal:
            modal_titulo = password_modal.text
            if modal_titulo == 'Senha do processo':
                should_get_2grau = False
                self.results['2grau'] = 'É necessário fornecer uma senha para acessar o processo.'
                return should_get_2grau
        else:
            should_get_2grau = True
            return should_get_2grau
            """
            print('nao tem alerta, liberado pra crawlear')
            xiripingo = soup.find('div', attrs={'id' : 'classeProcesso'}).text
            print(xiripingo)
            """

# LINK DIRETO
    def get_2grau_linkdireto(self, num_processo):
        num = num_processo
        should_get_2grau = self.check_2grau(f'https://www2.tjal.jus.br/cposg5/search.do?conversationId=&paginaConsulta=0&cbPesquisa=NUMPROC&numeroDigitoAnoUnificado={num[:15]}&foroNumeroUnificado={num[-4:]}&dePesquisaNuUnificado={num}&dePesquisaNuUnificado=UNIFICADO&dePesquisa=&tipoNuProcesso=UNIFICADO')

        if should_get_2grau == True:
            # num = num_processo
            name = self.sigla_tribunal
            urls_2grau = []
            if name == 'tjal':
                url_2grau = f'https://www2.tjal.jus.br/cposg5/search.do?conversationId=&paginaConsulta=0&cbPesquisa=NUMPROC&numeroDigitoAnoUnificado={num[:15]}&foroNumeroUnificado={num[-4:]}&dePesquisaNuUnificado={num}&dePesquisaNuUnificado=UNIFICADO&dePesquisa=&tipoNuProcesso=UNIFICADO'
                urls_2grau.append(url_2grau)
                # return urls_2grau
            else:
                url_2grau = f'https://esaj.tjce.jus.br/cposg5/search.do?conversationId=&paginaConsulta=0&cbPesquisa=NUMPROC&numeroDigitoAnoUnificado={num[:15]}&foroNumeroUnificado={num[-4:]}&dePesquisaNuUnificado={num}&dePesquisaNuUnificado=UNIFICADO&dePesquisa=&tipoNuProcesso=UNIFICADO'
                urls_2grau.append(url_2grau)
                # return urls_2grau
            try:
                for url in urls_2grau:
                    infos = self.extract_info_2grau(url)
                    # print(infos)
            except:
                return

# CONSULTA CLICANDO NO BOTAO
    def get_2grau_click(self, num_processo):
        num = num_processo
        should_get_2grau = self.check_2grau(f'https://www2.tjal.jus.br/cposg5/search.do?conversationId=&paginaConsulta=0&cbPesquisa=NUMPROC&numeroDigitoAnoUnificado={num[:15]}&foroNumeroUnificado={num[-4:]}&dePesquisaNuUnificado={num}&dePesquisaNuUnificado=UNIFICADO&dePesquisa=&tipoNuProcesso=UNIFICADO')

        if should_get_2grau == True:
            name = self.sigla_tribunal
            urls_2grau = []
            # num = '0007750-06.1992.8.02.0001' # tjal

            if name == 'tjal':
                url_search = f'https://www2.tjal.jus.br/cposg5/search.do?conversationId=&paginaConsulta=0&cbPesquisa=NUMPROC&numeroDigitoAnoUnificado={num[:15]}&foroNumeroUnificado={num[-4:]}&dePesquisaNuUnificado={num}&dePesquisaNuUnificado=UNIFICADO&dePesquisa=&tipoNuProcesso=UNIFICADO'
            else:
                url_search = f'https://esaj.tjce.jus.br/cposg5/search.do?conversationId=&paginaConsulta=0&cbPesquisa=NUMPROC&numeroDigitoAnoUnificado={num[:15]}&foroNumeroUnificado={num[-4:]}&dePesquisaNuUnificado={num}&dePesquisaNuUnificado=UNIFICADO&dePesquisa=&tipoNuProcesso=UNIFICADO'

            response = requests.get(url_search)
            content = response.content
            soup = BeautifulSoup(content, 'html.parser')
            botao_selecionar = soup.find_all('input', attrs={'id': 'processoSelecionado'})
            codigos = [input_tag['value'] for input_tag in botao_selecionar if not input_tag.find_parent('label', class_='list__dependentes_row')]

            for codigo in codigos:
                if name == 'tjal':
                    base_url = f'https://www2.tjal.jus.br/cposg5/show.do?processo.codigo={codigo}'
                else:
                    base_url = f'https://esaj.tjce.jus.br/cposg5/show.do?processo.codigo={codigo}'

                urls_2grau.append(base_url)
                # return urls_2grau

            try:
                for url in urls_2grau:
                    infos = self.extract_info_2grau(url)
                    print(infos)
            except:
                return
            
    def get_infos_2grau(self, num_processo):
        num = num_processo
        try:
            self.get_2grau_linkdireto(num)
            self.get_2grau_click(num)
            self.get_2grau_links(num)
        except:
            return

# CONSULTA PROCURANDO OS HREFS
    def get_2grau_links(self, num_processo):
        num = num_processo
        name = self.sigla_tribunal
        urls_2grau = []
        # num = '0001019-40.2012.8.02.0050'  # tjal

        if name == 'tjal':
            url_search = f'https://www2.tjal.jus.br/cposg5/search.do?conversationId=&paginaConsulta=0&cbPesquisa=NUMPROC&numeroDigitoAnoUnificado={num[:15]}&foroNumeroUnificado={num[-4:]}&dePesquisaNuUnificado={num}&dePesquisaNuUnificado=UNIFICADO&dePesquisa=&tipoNuProcesso=UNIFICADO'
        else:
            url_search = f'https://esaj.tjce.jus.br/cposg5/search.do?conversationId=&paginaConsulta=0&cbPesquisa=NUMPROC&numeroDigitoAnoUnificado={num[:15]}&foroNumeroUnificado={num[-4:]}&dePesquisaNuUnificado={num}&dePesquisaNuUnificado=UNIFICADO&dePesquisa=&tipoNuProcesso=UNIFICADO'

        response = requests.get(url_search)
        content = response.content
        soup = BeautifulSoup(content, 'html.parser')
        lista_processos = soup.find_all('a', attrs={'class': 'linkProcesso'})
        links = [link_tag['href'] for link_tag in lista_processos]

        for link in links:
            if name == 'tjal':
                url_2grau = 'https://www2.tjal.jus.br/' + link
            else:
                url_2grau = 'https://esaj.tjce.jus.br/' + link

            urls_2grau.append(url_2grau)
        
            try:
                for url in urls_2grau:
                    infos = self.extract_info_2grau(url)
                    print(infos)
            except:
                return



# INDICAÇÃO DE ERRO (NAO ACHOU)
# acho que vou fazer com o try 

    def extract_infos_2grau_tjal(self, num_processo):
        num = num_processo
        try:
            url = self.get_2grau_linkdireto(num)
            url = self.get_2grau_click(num)
            url = self.get_2grau_links(num)
        except:
            print('Não encontrei esse processo')

##### SEGUNDO GRAU TJCE #######
# LINK DIRETO

def get_2grau_link_direto_tjce():
    num = '0765717-73.2000.8.06.0001'
    url = f'https://esaj.tjce.jus.br/cposg5/search.do?conversationId=&paginaConsulta=0&cbPesquisa=NUMPROC&numeroDigitoAnoUnificado={num[:15]}&foroNumeroUnificado={num[-4:]}&dePesquisaNuUnificado={num}&dePesquisaNuUnificado=UNIFICADO&dePesquisa=&tipoNuProcesso=UNIFICADO'
    print(url)

    try:
        response = requests.get(url)
        content = response.content
        soup = BeautifulSoup(content, 'html.parser')
        classe_processo = soup.find('div', attrs={'id' : 'classeProcesso'}).text
        print(classe_processo)
    except:
        print('não encontrei esse processo')



# CONSULTA CLICANDO NO BOTAO

def clica_botao():
    num = '0051571-90.2016.8.06.0071'
    url = f'https://esaj.tjce.jus.br/cposg5/search.do?conversationId=&paginaConsulta=0&cbPesquisa=NUMPROC&numeroDigitoAnoUnificado={num[:15]}&foroNumeroUnificado={num[-4:]}&dePesquisaNuUnificado={num}&dePesquisaNuUnificado=UNIFICADO&dePesquisa=&tipoNuProcesso=UNIFICADO'
    print(url)

    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')
    botao_selecionar = soup.find_all('input', attrs={'id': 'processoSelecionado'})
    codes = [input_tag['value'] for input_tag in botao_selecionar if not input_tag.find_parent('label', class_='list__dependentes_row')]
    print(codes)

    urls = []
    for code in codes:
        base_url = f'https://esaj.tjce.jus.br/cposg5/show.do?processo.codigo={code}'
        urls.append(base_url)
        print(urls)


    for url in urls:
        try:
            response = requests.get(url)
            content = response.content
            soup = BeautifulSoup(content, 'html.parser')
            classe_processo = soup.find('div', attrs={'id': 'areaProcesso'}).text
            print(classe_processo)
        except:
            print('não encontrei esse processo')

# CONSULTA PROCURANDO OS HREFS
def get_2grau_links_tjce():
    num = '0001019-40.2012.8.02.0050'
    url = f'https://esaj.tjce.jus.br/cposg5/search.do?conversationId=&paginaConsulta=0&cbPesquisa=NUMPROC&numeroDigitoAnoUnificado={num[:15]}&foroNumeroUnificado={num[-4:]}&dePesquisaNuUnificado={num}&dePesquisaNuUnificado=UNIFICADO&dePesquisa=&tipoNuProcesso=UNIFICADO'
    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')
    lista_processos = soup.find_all('a', attrs={'class': 'linkProcesso'})
    links = [link_tag['href'] for link_tag in lista_processos]

    results = []

    for link in links:
        new_link = 'https://esaj.tjce.jus.br/' + link
        try:
            response = requests.get(new_link)
            content = response.content
            soup = BeautifulSoup(content, 'html.parser')
            classe_processo = soup.find('div', attrs={'id': 'areaProcesso'}).text
            results.append(classe_processo)
        except:
            print('não encontrei esse processo')


crawler_tjal = CrawlerTribunal('tjal')
crawler_tjal.get_infos_2grau('0007750-06.1992.8.02.0001')

"""
###### get Urls 1o grau do TJAL
'https://www2.tjal.jus.br/cpopg/show.do?processo.codigo=&processo.foro=1&processo.numero={num}' -- isso aqui já funciona;

Dados a serem coletados:
classe  (span id classeProcesso) 
área  (span)
assunto  (span)
data de distribuição  (div)
juiz  ()
valor da ação  ()
partes do processo  ()
lista das movimentações (data e movimento)  ()

###### get Urls do 2 grau do tjal

DOIS PASSOS:
1) abrir a consulta;
2) verificar se existem processos;
3) se tiver um, capturar o CÓDIGO, retornar o código e colocar na URL 
4) se tiver mais de um, capturar os HREFS, jogar numa lista e fazer um for pra que o crawler entre nos dois links e puxe as informações

Dados a serem coletados:
classe  (div id classeProcesso) 
área  (span)
assunto  (span)
data de distribuição  (div)
juiz  ()
valor da ação  ()
partes do processo  ()
lista das movimentações (data e movimento)  ()


###### get urls do 1 grau do tjce

Dados a serem coletados:
classe  ()
área  ()
assunto  ()
data de distribuição  ()
juiz  ()
valor da ação  ()
partes do processo  ()
lista das movimentações (data e movimento)  ()

###### get urls do 2 grau do tjc

Dados a serem coletados:

classe  ()
área  ()
assunto  ()
data de distribuição  ()
juiz  ()
valor da ação  ()
partes do processo  ()
lista das movimentações (data e movimento)  ()

"""
