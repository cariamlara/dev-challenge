import requests
from bs4 import BeautifulSoup
import re
import json

"""
def x():
    num_processo = '0763954-46.2014.8.06.0001'
    tribunal = 'tjce'
    placeholders = ['esaj', 'www2']
    if tribunal == 'tjce':
        base_url_1grau = f'https://{placeholders[0]}.{tribunal}.jus.br/cpopg/show.do?processo.codigo=&processo.foro={num_processo[-4:].lstrip("0")}&processo.numero={num_processo}'
        base_url_2grau = f'https://{placeholders[0]}.{tribunal}.jus.br/cposg5/search.do?conversationId=&paginaConsulta=0&cbPesquisa=NUMPROC&numeroDigitoAnoUnificado={num_processo[:15]}&foroNumeroUnificado={num_processo[-4:]}&dePesquisaNuUnificado={num_processo}&dePesquisaNuUnificado=UNIFICADO&dePesquisa=&tipoNuProcesso=UNIFICADO'
        return base_url_2grau
    else:
        base_url_1grau = f'https://{placeholders[1]}.{tribunal}.jus.br/cpopg/show.do?processo.codigo=&processo.foro=71&processo.numero='
        base_url_2grau = 'y'

url = x()
response = requests.get('https://esaj.tjce.jus.br/cposg5/search.do?conversationId=&paginaConsulta=0&cbPesquisa=NUMPROC&numeroDigitoAnoUnificado=0763954-46.2014&foroNumeroUnificado=1&dePesquisaNuUnificado=0763954-46.2014.8.06.0001&dePesquisaNuUnificado=UNIFICADO&dePesquisa=&tipoNuProcesso=UNIFICADO')
content = response.content
soup = BeautifulSoup(content, 'html.parser')
texto_qualquer = soup.find('div', attrs={'id': 'classeProcesso'}).text
print(texto_qualquer)
"""

def umafuncao():
    try:
        print(X)
    except:
        return
    else:
        print('nao consegui pegar')

def duas_func():
    y = 'jdsjds'
    try:
        print(y)
    except:
        print('deu td errado')


def tresfunc():
    try:
        umafuncao()
        duas_func()
    except:
        print('n funfou')

tresfunc()