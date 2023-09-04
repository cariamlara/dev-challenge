import requests
from bs4 import BeautifulSoup
import re
import json
 

class CrawlerTribunal():
    def __init__(self, sigla_tribunal):
        self.sigla_tribunal = sigla_tribunal
        self.results = {'1º grau': {}, 
                        '2º grau': {}}

    paths = [
            'classeProcesso',
            'areaProcesso',
            'assuntoProcesso',
            'dataHoraDistribuicaoProcesso',
            'juizProcesso',
            'valorAcaoProcesso',
            'tablePartesPrincipais',
            'tabelaUltimasMovimentacoes',
            ]
    
##########  PRIMEIRO GRAU  ##########

# FUNÇÃO PARA EXTRAIR INFORMAÇÕES DO SEGUNDO GRAU

    def extract_info_1degree(self, url):
        response = requests.get(url)
        content = response.content
        soup = BeautifulSoup(content, 'html.parser')
        check_if_exists = soup.find('span', attrs={'id' : 'numeroProcesso'})
        password_modal = soup.find('form', attrs={'id' : 'popupSenha'})
        
        resultados = {} 
        
        if check_if_exists:
            for path in self.paths:
                element = soup.find('span', attrs={'id': path}) or soup.find('div', attrs={'id': path})
                element_table_movimentacoes = soup.find('tbody', attrs={'id' : path})
                element_table_parties = soup.find('table', attrs={'id' : path})

                if element:
                    resultados[path] = str(element.text.replace("\n", "").replace("\t", "").replace("\xa0", ""))


                elif element_table_movimentacoes:
                    table_movimentacoes = {}
                    tr_elements = soup.find('tbody', id='tabelaUltimasMovimentacoes').find_all('tr')

                    for index, tr in enumerate(tr_elements):
                        date = tr.find('td', class_='dataMovimentacao').text.strip()
                        if date in table_movimentacoes:
                            date += f" ({index})"
                        
                        description_element = tr.find('td', class_='descricaoMovimentacao')

                        for span in description_element.find_all('span'):
                            span.extract()

                        description = description_element.text.strip()
                        table_movimentacoes[date] = description
                    
                    resultados[path] = table_movimentacoes


                elif element_table_parties:
                    info_parties = {}
                    tr_elements = soup.find('table', id='tablePartesPrincipais').find_all('tr')

                    for index, tr in enumerate(tr_elements):
                        role = tr.find('span', class_='tipoDeParticipacao').text.strip().replace("&nbsp;", "").replace("\n", "").replace("\t", "").replace("\xa0", "").replace(":", "")
                        party_element = tr.find('td', class_='nomeParteEAdvogado').text.strip().replace("&nbsp;", "").replace("\t", "").replace("\xa0", "").replace(":", "").replace('Advogado', "").replace('Advogada', "")
                        party_elements = party_element.split('<br>')
                        formatted_party_elements = []

                        for part in party_elements:
                            formatted_party_elements.extend(part.strip().split('\n'))

                        formatted_party_elements = [element.strip() for element in formatted_party_elements if element.strip()]
                        formatted_party_elements = [f'{element}' for element in formatted_party_elements]

                        if role not in info_parties:
                            info_parties[role] = formatted_party_elements
                            resultados[path] = info_parties
                        else:
                            info_parties[f'{role} ({index})'] = formatted_party_elements
                            resultados[path] = info_parties
                    
                else:
                    resultados[path] = 'Não consta'
                    
            self.results['1º grau'] = resultados
            return self.results

        elif password_modal:
            return 'É necessário fornecer uma senha para acessar o processo.'
    
        else:
            return 'Processo não encontrado.'
        
# FUNÇÃO QUE COLETA OS DADOS DO PROCESSO EM 1º GRAU (PARA O 1º GRAU NÃO É NECESSÁRIO CONSTRUIR DIFERENTES URLS)

    def get_1degree(self, num_processo):
        num = num_processo
        name = self.sigla_tribunal
        if name == 'tjal':
            url_1grau = f'https://www2.tjal.jus.br/cpopg/show.do?processo.codigo=&processo.foro={num[-4:].lstrip("0")}&processo.numero={num}'
        else:
            url_1grau = f'https://esaj.tjce.jus.br/cpopg/show.do?processo.codigo=&processo.foro={num[-4:].lstrip("0")}&processo.numero={num}'
        
        infos = self.extract_info_1degree(url_1grau)
        return infos

##### SEGUNDO GRAU

# FUNÇÃO PARA CHECAR SE O PROCESSO EXISTE EM SEGUNDO GRAU

    def check_2grau(self, numero_processo):
        num = numero_processo
        nome_tribunal = self.sigla_tribunal

        if nome_tribunal == 'tjal':
            url = f'https://www2.tjal.jus.br/cposg5/search.do?conversationId=&paginaConsulta=0&cbPesquisa=NUMPROC&numeroDigitoAnoUnificado={num[:15]}&foroNumeroUnificado={num[-4:]}&dePesquisaNuUnificado={num}&dePesquisaNuUnificado=UNIFICADO&dePesquisa=&tipoNuProcesso=UNIFICADO'
        else:
            url = f'https://esaj.tjce.jus.br/cposg5/search.do?conversationId=&paginaConsulta=0&cbPesquisa=NUMPROC&numeroDigitoAnoUnificado={num[:15]}&foroNumeroUnificado={num[-4:]}&dePesquisaNuUnificado={num}&dePesquisaNuUnificado=UNIFICADO&dePesquisa=&tipoNuProcesso=UNIFICADO'

        response = requests.get(url)
        content = response.content
        soup = BeautifulSoup(content, 'html.parser')
        alert = soup.find('td', attrs={'role' : 'alert'})
        password_modal = soup.find('form', attrs={'id' : 'popupSenha'})

        if alert:
            should_get_2grau = False
            self.results['2º grau'] = 'Esse processo não tem 2 grau.'
            return should_get_2grau
        
        elif password_modal:
            should_get_2grau = False
            self.results['2grau'] = 'É necessário fornecer uma senha para acessar o processo.'
            return should_get_2grau
        
        else:
            should_get_2grau = True
            return should_get_2grau
        
# FUNÇÃO PARA EXTRAIR INFORMAÇÕES DO SEGUNDO GRAU

    def extract_info_2degree(self, url):
        response = requests.get(url)
        content = response.content
        soup = BeautifulSoup(content, 'html.parser')
        check_if_exists = soup.find('span', attrs={'id' : 'numeroProcesso'})
        
        resultados = {} 

        if check_if_exists:
            for path in self.paths:
                element = soup.find('span', attrs={'id': path}) or soup.find('div', attrs={'id': path})
                element_table_movimentacoes = soup.find('tbody', attrs={'id' : path})
                element_table_parties = soup.find('table', attrs={'id' : path})

                if element:
                    resultados[path] = str(element.text.replace("\n", "").replace("\t", "").replace("\xa0", ""))

                elif element_table_movimentacoes:
                    table_movimentacoes = {}
                    tr_elements = soup.find('tbody', id='tabelaUltimasMovimentacoes').find_all('tr')

                    for index, tr in enumerate(tr_elements):
                        date = tr.find('td', class_='dataMovimentacaoProcesso').text.strip()
                        if date in table_movimentacoes:
                            date += f" ({index})"
                        
                        description_element = tr.find('td', class_='descricaoMovimentacaoProcesso')

                        for span in description_element.find_all('span'):
                            span.extract()

                        description = description_element.text.strip()
                        table_movimentacoes[date] = description
                    
                    resultados[path] = table_movimentacoes

                elif element_table_parties:
                    info_parties = {}
                    tr_elements = soup.find('table', id='tablePartesPrincipais').find_all('tr')

                    for index, tr in enumerate(tr_elements):
                        role = tr.find('span', class_='tipoDeParticipacao').text.strip().replace("&nbsp;", "").replace("\n", "").replace("\t", "").replace("\xa0", "").replace(":", "")
                        party_element = tr.find('td', class_='nomeParteEAdvogado').text.strip().replace("&nbsp;", "").replace("\t", "").replace("\xa0", "").replace(":", "").replace('Advogado', "").replace('Advogada', "")
                        party_elements = party_element.split('<br>')
                        formatted_party_elements = []

                        for part in party_elements:
                            formatted_party_elements.extend(part.strip().split('\n'))

                        formatted_party_elements = [element.strip() for element in formatted_party_elements if element.strip()]
                        formatted_party_elements = [f'{element}' for element in formatted_party_elements]

                        if role not in info_parties:
                            info_parties[role] = formatted_party_elements
                            resultados[path] = info_parties
                        else:
                            info_parties[f'{role} ({index})'] = formatted_party_elements
                            resultados[path] = info_parties
                else:
                    resultados[path] = 'Não consta'

            self.results['2º grau'] = resultados
            return self.results
        else:
            return
                

#  FUNÇÃO QUE QUE PEGA A URL DIRETA DO PROCESSO, SEM PRECISAR DE CONSTRUÇÃO

    def get_2grau_linkdireto(self, num_processo):
        num = num_processo
        should_get_2grau = self.check_2grau(num)

        if should_get_2grau == True:
            name = self.sigla_tribunal
            urls_2grau = []
            if name == 'tjal':
                url_2grau = f'https://www2.tjal.jus.br/cposg5/search.do?conversationId=&paginaConsulta=0&cbPesquisa=NUMPROC&numeroDigitoAnoUnificado={num[:15]}&foroNumeroUnificado={num[-4:]}&dePesquisaNuUnificado={num}&dePesquisaNuUnificado=UNIFICADO&dePesquisa=&tipoNuProcesso=UNIFICADO'
                urls_2grau.append(url_2grau)
            else:
                url_2grau = f'https://esaj.tjce.jus.br/cposg5/search.do?conversationId=&paginaConsulta=0&cbPesquisa=NUMPROC&numeroDigitoAnoUnificado={num[:15]}&foroNumeroUnificado={num[-4:]}&dePesquisaNuUnificado={num}&dePesquisaNuUnificado=UNIFICADO&dePesquisa=&tipoNuProcesso=UNIFICADO'
                urls_2grau.append(url_2grau)
            try:
                for url in urls_2grau:
                    infos = self.extract_info_2degree(url)
                    return infos
            except:
                return

#  FUNÇÃO QUE CONSTRÓI A URL A PARTIR DO BOTÃO DE SELECIONAR PROCESSO

    def get_2grau_click(self, num_processo):
        num = num_processo
        should_get_2grau = self.check_2grau(num)

        if should_get_2grau == True:
            name = self.sigla_tribunal
            urls_2grau = []

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

            try:
                for url in urls_2grau:
                    infos = self.extract_info_2degree(url)
                    return infos
            except:
                return
            
# FUNÇÃO QUE CONSTRÓI A URL A PARTIR DOS LINKS HREF DA PÁGINA DE CONSULTA

    def get_2grau_links(self, num_processo):
        num = num_processo
        name = self.sigla_tribunal
        urls_2grau = []

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
                    return infos
            except:
                return
            
# FUNÇÃO QUE TESTA TODOS OS MÉTODOS DE ENCONTRAR A URL DO 2º GRAU E GERA AS INFORMAÇÕES A PARTIR DO LINK CORRETO
    def get_infos_2degree(self, num_processo):
        num = num_processo
        try:
            self.get_2grau_linkdireto(num)
            self.get_2grau_click(num)
            self.get_2grau_links(num)
        except:
            self.results['2º grau' : 'Esse processo não foi encontrado em 2º grau.']


# FUNÇÃO QUE BUSCA O PROCESSO EM TODOS OS GRAUS E COLETA AS INFORMAÇÕES
    def collect_all_infos(self, num_processo):
        num = num_processo
        infos_1grau = self.get_1degree(num)
        infos_2grau = self.get_infos_2degree(num)
        return infos_1grau, infos_2grau
    