import logging
import json

from linkedin_jobs_scraper import LinkedinScraper
from linkedin_jobs_scraper.events import Events, EventData, EventMetrics
from linkedin_jobs_scraper.query import Query, QueryOptions, QueryFilters
from linkedin_jobs_scraper.filters import RelevanceFilters, TimeFilters, TypeFilters, ExperienceLevelFilters, \
    OnSiteOrRemoteFilters

# Change root logger level (default is WARN)
logging.basicConfig(level=logging.INFO)

# Lista para armazenar as vagas encontradas
found_jobs = []


def salvar(data: EventData):
    # Verifica se já existe uma vaga com o mesmo job_id
    if any(job['job_id'] == data.job_id for job in found_jobs):
        return

    # Cria um dicionário com as métricas da vaga
    job = {
        'job_id': data.job_id,
        'link': data.link,
        'apply_link': data.apply_link,
        'title': data.title,
        'company': data.company,
        'company_link': data.company_link,
        'company_img_link': data.company_img_link,
        'place': data.place,
        'description': data.description,
        'description_html': data.description_html,
        'date': data.date,
        'insights': data.insights
    }
    # Adiciona a vaga à lista
    found_jobs.append(job)


# Fired once for each successfully processed job
def on_data(data: EventData):
    print('[ON_DATA]', data.title, data.company, data.company_link, data.date, data.link, data.insights,
          len(data.description))
    salvar(data)


# Fired once for each page (25 jobs)
def on_metrics(metrics: EventMetrics):
    print('[ON_METRICS]', str(metrics))


def on_error(error):
    print('[ON_ERROR]', error)


def on_end():
    print('[ON_END]')
    with open('vagas_linkedin.json', 'w') as f:
        json.dump(found_jobs, f, indent=4)


def run_linkedin_scraper():
    scraper = LinkedinScraper(
        chrome_executable_path=None,  # Custom Chrome executable path (e.g. /foo/bar/bin/chromedriver)
        chrome_options=None,  # Custom Chrome options here
        headless=True,  # Overrides headless mode only if chrome_options is None
        max_workers=1,  # How many threads will be spawned to run queries concurrently (one Chrome driver for each thread)
        slow_mo=1,  # Slow down the scraper to avoid 'Too many requests 429' errors (in seconds)
        page_load_timeout=40  # Page load timeout (in seconds)
    )

    # Add event listeners
    scraper.on(Events.DATA, on_data)
    scraper.on(Events.ERROR, on_error)
    scraper.on(Events.END, on_end)

    queries = [
        Query(
            query='Estágio engenharia de telecomunicações',
            options=QueryOptions(
                locations=['Rio de Janeiro'],
                apply_link=True,
                # Try to extract apply link (easy applies are skipped). If set to True, scraping is slower because an additional page must be navigated. Default to False.
                skip_promoted_jobs=True,  # Skip promoted jobs. Default to False.
                page_offset=0,  # How many pages to skip
                limit=5,
                filters=QueryFilters(
                    relevance=RelevanceFilters.RECENT,
                    time=TimeFilters.ANY

                )
            )
        ),
        Query(
            query='Estágio engenharia de telecomunicações',
            options=QueryOptions(
                locations=['Brazil'],
                apply_link=True,
                # Try to extract apply link (easy applies are skipped). If set to True, scraping is slower because an additional page must be navigated. Default to False.
                skip_promoted_jobs=True,  # Skip promoted jobs. Default to False.
                page_offset=0,  # How many pages to skip
                limit=5,
                filters=QueryFilters(
                    relevance=RelevanceFilters.RECENT,
                    time=TimeFilters.ANY,
                    on_site_or_remote=[OnSiteOrRemoteFilters.REMOTE]

                )
            )
        ),
    ]

    scraper.run(queries)


# Executa o LinkedIn scraper
run_linkedin_scraper()



'''import logging
import json

from linkedin_jobs_scraper import LinkedinScraper
from linkedin_jobs_scraper.events import Events, EventData, EventMetrics
from linkedin_jobs_scraper.query import Query, QueryOptions, QueryFilters
from linkedin_jobs_scraper.filters import RelevanceFilters, TimeFilters, TypeFilters, ExperienceLevelFilters, \
    OnSiteOrRemoteFilters

# Change root logger level (default is WARN)
logging.basicConfig(level=logging.INFO)

# Lista para armazenar as vagas encontradas
found_jobs = []


def salvar(data: EventData):
    # Verifica se já existe uma vaga com o mesmo job_id
    if any(job['job_id'] == data.job_id for job in found_jobs):
        return

    # Cria um dicionário com as métricas da vaga
    job = {
        'job_id': data.job_id,
        'link': data.link,
        'apply_link': data.apply_link,
        'title': data.title,
        'company': data.company,
        'company_link': data.company_link,
        'company_img_link': data.company_img_link,
        'place': data.place,
        'description': data.description,
        'description_html': data.description_html,
        'date': data.date,
        'insights': data.insights
    }
    # Adiciona a vaga à lista
    found_jobs.append(job)


# Fired once for each successfully processed job
def on_data(data: EventData):
    print('[ON_DATA]', data.title, data.company, data.company_link, data.date, data.link, data.insights,
          len(data.description))
    salvar(data)


# Fired once for each page (25 jobs)
def on_metrics(metrics: EventMetrics):
    print('[ON_METRICS]', str(metrics))


def on_error(error):
    print('[ON_ERROR]', error)


def on_end():
    print('[ON_END]')
    with open('vagas_linkedin.json', 'w') as f:
        json.dump(found_jobs, f, indent=4)


scraper = LinkedinScraper(
    chrome_executable_path=None,  # Custom Chrome executable path (e.g. /foo/bar/bin/chromedriver)
    chrome_options=None,  # Custom Chrome options here
    headless=True,  # Overrides headless mode only if chrome_options is None
    max_workers=1,  # How many threads will be spawned to run queries concurrently (one Chrome driver for each thread)
    slow_mo=1,  # Slow down the scraper to avoid 'Too many requests 429' errors (in seconds)
    page_load_timeout=40  # Page load timeout (in seconds)
)

# Add event listeners
scraper.on(Events.DATA, on_data)
scraper.on(Events.ERROR, on_error)
scraper.on(Events.END, on_end)

queries = [
    Query(
        query='Estágio engenharia de telecomunicações',
        options=QueryOptions(
            locations=['Rio de Janeiro'],
            apply_link=True,
            # Try to extract apply link (easy applies are skipped). If set to True, scraping is slower because an additional page mus be navigated. Default to False.
            skip_promoted_jobs=True,  # Skip promoted jobs. Default to False.
            page_offset=0,  # How many pages to skip
            limit=5,
            filters=QueryFilters(
                relevance=RelevanceFilters.RECENT,
                time=TimeFilters.ANY

            )
        )
    ),
    Query(
        query='Estágio engenharia de telecomunicações',
        options=QueryOptions(
            locations=['Brazil'],
            apply_link=True,
            # Try to extract apply link (easy applies are skipped). If set to True, scraping is slower because an additional page mus be navigated. Default to False.
            skip_promoted_jobs=True,  # Skip promoted jobs. Default to False.
            page_offset=0,  # How many pages to skip
            limit=5,
            filters=QueryFilters(
                relevance=RelevanceFilters.RECENT,
                time=TimeFilters.ANY,
                on_site_or_remote=[OnSiteOrRemoteFilters.REMOTE]

            )
        )
    ),
]

scraper.run(queries)



'''