# Dev challenge Jus - Crawlers para o TJCE e TJAL
Neste projeto eu construí um crawler que extrai informações sobre processos em 1º e 2º grau dos sites dos tribunais do Ceará e do Alagoas (TJCE e TJAL, respectivamente).

## Estrutura geral do projeto:

- Arquivo principal da aplicação: ```app.py```
   - Aqui foi realizada a construção da API que receberá um JSON contendo o número do processo desejado e que fará a requisição aos crawlers;
     
- Arquivo secundário: ```crawlers.py```
   - Contém a classe construída para extrair as informações.

 ### Dados a serem extraídos:
```
Classe
Área
Assunto
Data de distribuição
Juiz
Valor da ação
Partes do processo
Lista das movimentações (data e movimento)
```

## Requisitos
- python (estou usando a versão 3.10.4)
- pip
- Flask
- beautifulsoup4
- requests
- Postman (https://www.postman.com/downloads/)

## Instalação e execução
> Estou utilizando o sistema operacional **Windows**

1. Clone o repositório na sua máquina
3. Navegue até a pasta do projeto
5. Ative o ambiente virtual

```
venv\Scripts\activate
```

6. Instale as dependências

```
pip install -r requirements.txt
```

7. Execute o projeto
   
_Utilizando o prompt de comando, abra a pasta do projeto e rode o seguinte comando_
```
python app.py
```
  
![image](https://github.com/cariamlara/dev-challenge/assets/85589143/9e560198-69ba-4d97-af9f-e7d8974e48b3)

> **Se estiver tudo certo, a API deve estar pronta pra usar :)** 

## Consultando o processo
1. Abra o Postman
2. Faça uma requisição PUT no endereço ```http://127.0.0.1:5000/processos``` passando um JSON no Body (raw) contendo o número do processo como parâmetro, dessa forma:
```{ "numero_processo" : "0170599-97.2018.8.06.0001" }```

![image](https://github.com/cariamlara/dev-challenge/assets/85589143/90838a67-d724-4952-9b8b-e31bfd2bd9d9)


_Alguns números que você pode utilizar:_
- _0721604-73.2022.8.02.0001_
- _0710802-55.2018.8.02.0001_ 
- _0170599-97.2018.8.06.0001_
- _0113248-06.2017.8.06.0001_
- _0026060-03.2010.8.06.0071_ 

# Considerações finais

Gostei muito de realizar o desafio :D 

Apesar de não ter sido simples, me diverti construindo o projeto. Essa é uma primeira versão dele, que acabou ficando bem simplezinha porque tentei construir algo minimamente funcional antes de começar a incrementar com outras coisas (como banco de dados, testes, etc -- ainda não sei fazer nada disso, preciso aprender).
Mas pretendo continuar trabalhando nele pra construir algo mais robusto e organizado. Por enquanto vou ficar feliz que consegui fazer alguma coisa kkkk.

Minha maior dificuldade foi na construção das URLs que servem de parâmetro para o requests, já que a consulta dos processos pode ser feita de várias formas diferentes, e cada forma gera um tipo de HTML diferente.
Também tive algumas complicações em relação a formatação de texto. Se possível, adoraria receber um feedback com sugestões de melhorias e indicações do que aprender pra me aperfeiçoar.

Obrigada pela oportunidade <3
