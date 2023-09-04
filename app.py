from flask import Flask, jsonify, request
from crawlers import CrawlerTribunal
import json

app = Flask(__name__)

crawler_tjce = CrawlerTribunal('tjce')
crawler_tjal = CrawlerTribunal('tjal') 

@app.route('/processos', methods=['PUT'])
def get_num_processo():
    num_processo = request.get_json()
    num = str(num_processo['numero_processo'])

    if num[16:20] == '8.06':
        resultado = crawler_tjce.collect_all_infos(num)
        return jsonify(resultado)
    elif num[16:20] == '8.02':
        resultado = crawler_tjal.collect_all_infos(num)
        return jsonify(resultado)
    else:
        return 'Esse processo não foi encontrado. Certifique-se de que está informando o número correto.'

app.run()
