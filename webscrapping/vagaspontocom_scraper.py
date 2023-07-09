import requests
from bs4 import BeautifulSoup
import json

# URL da pesquisa de estágios de engenharia de telecomunicações no Vagas.com.br
url = 'https://www.vagas.com.br/vagas-de-estagio-engenharia-de-telecomunicacoes?e%5B%5D=Rio+de+Janeiro&mo%5B%5D=Est%C3%A1gio'

# Faz a requisição GET para a URL da pesquisa
response = requests.get(url)

# Verifica se a requisição foi bem sucedida
if response.status_code == 200:
    # Parseia o conteúdo HTML da página
    soup = BeautifulSoup(response.content, 'html.parser')

    # Encontra todas as li que contêm as informações das vagas
    vagas = soup.find_all('li', class_='vaga')

    # Lista para armazenar os dados das vagas
    vagas_data = []

    # Itera sobre as vagas encontradas
    for vaga in vagas:
        # Extrai as informações da vaga
        titulo = vaga.find('h2', class_='cargo').text.strip()
        descricao = vaga.find('div', class_='detalhes').p.text.strip()
        empresa = vaga.find('span', class_='emprVaga').text.strip()
        link = vaga.find('a', class_='link-detalhes-vaga')['href']

        # Adiciona o prefixo "https://www.vagas.com.br" ao link da vaga
        link = f"https://www.vagas.com.br{link}"

        # Cria um dicionário com as informações da vaga
        vaga_data = {
            "title": titulo,
            "description": descricao,
            "company": empresa,
            "link": link
        }

        # Adiciona o dicionário à lista de dados das vagas
        vagas_data.append(vaga_data)

    # Salva os dados das vagas em um arquivo JSON
    with open('vagas_vagaspontocom.json', 'w') as file:
        json.dump(vagas_data, file)

else:
    print('Erro ao acessar a página:', response.status_code)
