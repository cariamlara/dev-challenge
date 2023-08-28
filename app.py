from flask import Flask, jsonify, request
from crawlers import CrawlerTribunal
import json

app = Flask(__name__)

crawler_tjal = CrawlerTribunal('tjal', "https://www2.tjal.jus.br/cpopg/show.do?processo.codigo=[0-9A-Z]{12}&processo.foro=1&processo.numero=")
# crawler_tjal.get_url("0001557-39.2012.8.02.0044")

@app.route('/processos', methods=['PUT'])
def get_num_proc():
    num_proc_json = request.get_json()
    num_proc = num_proc_json["num"]
    resultado = crawler_tjal.get_url(str(num_proc))
    return jsonify(resultado)

app.run()



