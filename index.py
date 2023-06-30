import os
from flask import Flask, render_template, request, json

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/vagas')
def vagas():

    json_file = os.path.join(os.path.dirname(__file__),  'jobs.json')

    # Lê o arquivo JSON
    with open(json_file, 'r') as file:
        data = json.load(file)

    # Retorne a página HTML renderizada com as informações do JSON
    return render_template('vagas.html', data=data)


if __name__ == '__ main__':
    app.run()
