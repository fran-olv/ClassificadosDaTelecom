import json
import subprocess
import multiprocessing
import schedule
import time


def executar_script_scraper(caminho_script, arquivo_saida):
    subprocess.run(["python", caminho_script, arquivo_saida])


def combinar_arquivos_json(arquivos_json):
    dados_combinados = []

    for arquivo in arquivos_json:
        with open(arquivo, 'r', encoding='utf-8') as arquivo_json:
            dados = json.load(arquivo_json)
            dados_combinados.extend(dados)

    return dados_combinados


def remover_vagas_duplicadas(vagas):
    vagas_unicas = []

    for vaga in vagas:
        if vaga not in vagas_unicas:
            vagas_unicas.append(vaga)

    return vagas_unicas


def realizar_scraping():
    scripts_scraper = [
        {"script": "linkedin_scraper.py", "output_file": "vagas_linkedin.json"},
        {"script": "vagaspontocom_scraper.py", "output_file": "vagas_vagaspontocom.json"},
        {"script": "infojobs_scraper.py", "output_file": "vagas_infojobs.json"},
        {"script": "googlejobs_scraper.py", "output_file": "vagas_googlejobs.json"}
    ]

    arquivos_json = []

    # Cria um pool de processos com o número de processos igual ao número de scripts de scraping
    pool = multiprocessing.Pool(processes=len(scripts_scraper))

    # Executa os scripts de scraping em paralelo
    for script in scripts_scraper:
        pool.apply_async(executar_script_scraper, args=(script["script"], script["output_file"]))

    # Aguarda a conclusão de todos os processos
    pool.close()
    pool.join()

    # Adiciona os arquivos JSON gerados à lista
    arquivos_json = [script["output_file"] for script in scripts_scraper]

    # Combina os dados de todos os arquivos JSON
    dados_combinados = combinar_arquivos_json(arquivos_json)

    # Remove vagas duplicadas com base nos critérios especificados
    vagas_unicas = remover_vagas_duplicadas(dados_combinados)

    # Salva os resultados em um novo arquivo JSON
    with open('vagas.json', 'w', encoding='utf-8') as arquivo_json:
        json.dump(vagas_unicas, arquivo_json, indent=2, ensure_ascii=False)

    print("Arquivo JSON de vagas combinadas criado com sucesso!")


def executar_tarefa_scraping():
    while True:
        realizar_scraping()
        time.sleep(1800)  # Espera 30 minutos

if __name__ == '__main__':
    executar_tarefa_scraping()
