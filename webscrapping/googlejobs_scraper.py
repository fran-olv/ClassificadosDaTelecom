import time
import json
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from parsel import Selector
from urllib.parse import quote


def scroll_page(url):
    # Configurar opções do ChromeDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Execução em segundo plano
    options.add_argument('--lang=en')   # Definir idioma como inglês
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36")  # Definir o user agent

    # Inicializar o ChromeDriver
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get(url)

    # Aguardar o carregamento completo da página
    time.sleep(3)

    # Encontrar e clicar no elemento do raio de busca
    radius_button = driver.find_element_by_css_selector('.TRwkpf[data-value="100.0"]')
    radius_button.click()

    # Obter a altura da página
    old_height = driver.execute_script("""
        function getHeight() {
            return document.querySelector('.zxU94d').scrollHeight;
        }
        return getHeight();
    """)

    # Rolagem da página até o final
    while True:
        driver.execute_script("document.querySelector('.zxU94d').scrollTo(0, document.querySelector('.zxU94d').scrollHeight)")

        time.sleep(2)

        # Obter a nova altura da página após a rolagem
        new_height = driver.execute_script("""
            function getHeight() {
                return document.querySelector('.zxU94d').scrollHeight;
            }
            return getHeight();
        """)

        # Verificar se a altura da página permaneceu a mesma após a rolagem
        if new_height == old_height:
            break

        old_height = new_height

    # Obter o conteúdo da página após a rolagem
    selector = Selector(driver.page_source)
    driver.quit()

    return selector


def scrape_google_jobs(selector):
    google_jobs_results = []

    for result in selector.css('.iFjolb'):
        # Obter o título e a empresa da vaga
        title = result.css('.BjJfJf::text').get()
        company = result.css('.vNEEBe::text').get()

        # Obter informações adicionais
        container = result.css('.Qk80Jf::text').getall()
        location = container[0]
        via = container[1]

        thumbnail = result.css('.pJ3Uqf img::attr(src)').get()
        extensions = result.css('.KKh3md span::text').getall()

        # Buscar link ou criar URL de busca
        link_element = result.css('a[data-ved]::attr(href)')
        link = link_element.get() if link_element else ''

        if not link:
            search_title = quote(title)
            params = {
                'q': search_title,                           # título da vaga como termo de pesquisa
                'ibp': 'htl;jobs',                            # busca por vagas de emprego no Google
                'uule': 'w+CAIQICJSaW9qZW4gSmFuZWVywqBv',      # localização codificada (Rio de Janeiro)
                'hl': 'pt-BR',                                # idioma
                'gl': 'br',                                   # país da pesquisa
                'htilrad': '100.0',                           # raio de busca de 100 km
            }
            search_url = f"https://www.google.com/search?q={params['q']}&ibp={params['ibp']}&uule={params['uule']}&hl={params['hl']}&gl={params['gl']}&htilrad={params['htilrad']}"
            link = search_url

        # Adicionar os resultados da vaga à lista
        google_jobs_results.append({
            'job_id': '',
            'link': link,
            'apply_link': '',
            'title': title,
            'company': company,
            'company_link': '',
            'company_img_link': '',
            'place': location,
            'description': '',
            'description_html': '',
            'date': '',
            'insights': []
        })

    return google_jobs_results


def run_google_scraper():
    params = {
        'q': 'Estágio Engenharia de Telecomunicações',     # termo de pesquisa
        'ibp': 'htl;jobs',                                # busca por vagas de emprego no Google
        'uule': 'w+CAIQICJSaW9qZW4gSmFuZWVywqBv',          # localização codificada (Rio de Janeiro)
        'hl': 'pt-BR',                                    # idioma
        'gl': 'br',                                       # país da pesquisa
    }

    # Montar a URL de pesquisa
    URL = f"https://www.google.com/search?q={params['q']}&ibp={params['ibp']}&uule={params['uule']}&hl={params['hl']}&gl={params['gl']}"
    print(URL)

    # Realizar a rolagem da página e obter o conteúdo
    result = scroll_page(URL)

    # Extrair os resultados das vagas de emprego
    google_jobs_results = scrape_google_jobs(result)

    # Salvar os resultados em um arquivo JSON
    json_data = json.dumps(google_jobs_results, indent=2, ensure_ascii=False)
    with open('vagas_googlejobs.json', 'w', encoding='utf-8') as json_file:
        json_file.write(json_data)

    print("Arquivo JSON criado com sucesso!")


# Executa o Google scraper
run_google_scraper()


