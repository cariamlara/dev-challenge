import requests
from bs4 import BeautifulSoup
import re
 
def url_1grau_tjal():
    num = '0007750-06.1992.8.02.0001'
    url = f'https://www2.tjal.jus.br/cpopg/show.do?processo.codigo=&processo.foro={num[-4:].lstrip("0")}&processo.numero={num}'
    print(url)

def url_1grau_tjce():
    num = '0051575-54.2021.8.06.0071'
    url = f'https://esaj.tjce.jus.br/cpopg/show.do?processo.codigo=&processo.foro={num[-4:].lstrip("0")}&processo.numero={num}'
    print(url)



##### SEGUNDO GRAU TJAL #######
# LINK DIRETO
def get_2grau_linkdireto():
    num = '0721604-73.2022.8.02.0001'
    url = f'https://www2.tjal.jus.br/cposg5/search.do?conversationId=&paginaConsulta=0&cbPesquisa=NUMPROC&numeroDigitoAnoUnificado={num[:15]}&foroNumeroUnificado={num[-4:]}&dePesquisaNuUnificado={num}&dePesquisaNuUnificado=UNIFICADO&dePesquisa=&tipoNuProcesso=UNIFICADO'
    print(url)

# CONSULTA CLICANDO NO BOTAO
def get_2grau_click():
    num = '0007750-06.1992.8.02.0001'
    url = f'https://www2.tjal.jus.br/cposg5/search.do?conversationId=&paginaConsulta=0&cbPesquisa=NUMPROC&numeroDigitoAnoUnificado={num[:15]}&foroNumeroUnificado={num[-4:]}&dePesquisaNuUnificado={num}&dePesquisaNuUnificado=UNIFICADO&dePesquisa=&tipoNuProcesso=UNIFICADO'
    print(url)

    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')
    botao_selecionar = soup.find_all('input', attrs={'id': 'processoSelecionado'})
    codes = [input_tag['value'] for input_tag in botao_selecionar if not input_tag.find_parent('label', class_='list__dependentes_row')]
    print(codes)

    urls = []
    for code in codes:
        base_url = f'https://www2.tjal.jus.br/cposg5/show.do?processo.codigo={code}'
        urls.append(base_url)
        print(urls)


    for url in urls:
        response = requests.get(url)
        content = response.content
        soup = BeautifulSoup(content, 'html.parser')
        classe_processo = soup.find('div', attrs={'id': 'areaProcesso'}).text
        print(classe_processo)

# CONSULTA PROCURANDO OS HREFS
def get_2grau_links():
    num = '0001019-40.2012.8.02.0050'
    url = f'https://www2.tjal.jus.br/cposg5/search.do?conversationId=&paginaConsulta=0&cbPesquisa=NUMPROC&numeroDigitoAnoUnificado={num[:15]}&foroNumeroUnificado={num[-4:]}&dePesquisaNuUnificado={num}&dePesquisaNuUnificado=UNIFICADO&dePesquisa=&tipoNuProcesso=UNIFICADO'
    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')
    lista_processos = soup.find_all('a', attrs={'class': 'linkProcesso'})
    links = [link_tag['href'] for link_tag in lista_processos]

    results = []

    for link in links:
        new_link = 'https://www2.tjal.jus.br/' + link
        response = requests.get(new_link)
        content = response.content
        soup = BeautifulSoup(content, 'html.parser')
        classe_processo = soup.find('div', attrs={'id': 'areaProcesso'}).text
        results.append(classe_processo)



# INDICAÇÃO DE ERRO (NAO ACHOU)
# acho que vou fazer com o try 

def extract_infos_2grau_tjal():
    pass

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