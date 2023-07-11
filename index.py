import os
from flask import Flask, render_template, request, json
import socket

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/vagas')
def vagas():
    json_file = os.path.join(os.path.dirname(__file__), 'webscrapping/vagas.json')

    # Lê o arquivo JSON
    with open(json_file, 'r') as file:
        data = json.load(file)

    # Retorne a página HTML renderizada com as informações do JSON
    return render_template('vagas.html', data=data)

#export FLASK_APP=index.py



if __name__ == '__ main__':

    #ip_publico = requests.get('https://api.ipify.org/').text
    #print(f'IP Publico: {ip_publico}')
    #host='10.1.124.206'
    #comando: flask run
    app.run(host='0.0.0.0')
