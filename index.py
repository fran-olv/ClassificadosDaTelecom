from flask import Flask, render_template
#from webscrapping_linkedin import scrape_linkedin

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


#@app.route("/vagas")
#def vagas():
    # Chama as funções de web scraping para obter os dados das vagas
#    resultados_linkedin = scrape_linkedin()
    #resultados_indeed = scrape_indeed()
    #resultados_google = scrape_google_vagas()

    # Concatena os resultados das três fontes de vagas
#    resultados_totais = resultados_linkedin + resultados_indeed + resultados_google

    # Renderiza o template HTML com os dados
#    return render_template("vagas.html", vagas=resultados_totais)

if __name__ == '__main__':
    app.run()


