import requests
from bs4 import BeautifulSoup
import json

# URL da pesquisa de estágios de engenharia de telecomunicações no InfoJobs
url = 'https://www.infojobs.com.br/vagas.aspx?palabra=est%C3%A1gio+de+engenharia+de+telecomunica%C3%A7%C3%B5es&provincia=182&tipocontrato=4&iv=8822151'

# Faz a requisição GET para a URL da pesquisa
response = requests.get(url)

# Verifica se a requisição foi bem sucedida
if response.status_code == 200:
    # Parseia o conteúdo HTML da página
    soup = BeautifulSoup(response.content, 'html.parser')

    # Encontra todas as divs que contêm as informações das vagas
    vagas = soup.find_all('div', class_='card-shadow-hover')

    # Lista para armazenar os dados das vagas
    vagas_data = []

    # Itera sobre as vagas encontradas
    for vaga in vagas:
        # Extrai as informações da vaga
        titulo = vaga.find('h2', class_='h3').text.strip()
        descricao = vaga.find('div', class_='small text-medium').text.strip()
        empresa = vaga.find('a', class_='text-body text-decoration-none').text.strip()
        link = vaga.find('a', class_='text-decoration-none')['href']

        # Adiciona o prefixo "https://www.vagas.com.br" ao link da vaga
        link = f"https://www.infojobs.com.br{link}"

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
    with open('vagas_infojobs.json', 'w') as file:
        json.dump(vagas_data, file)

else:
    print('Erro ao acessar a página:', response.status_code)