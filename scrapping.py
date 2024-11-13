"""Scrapping de escolas do Brasil"""

import json
import time
import unicodedata

import requests
from bs4 import BeautifulSoup

from scheduler import RequestOrder, Scheduler

# TODO: Fazer o JSON aninhado com informações do Ranking de competitividade
# TODO: Tirar a flag `possui_eja` (redundante)
# TODO: Fazer gráficos sobre os dados
# TODO: Passar pro chatGPT para que ele relacione os dados/ definir aplicação que usaria esses dados

# Número de escolas por cidade
# Rio das Ostras - RJ -> 107
# Paranaguá - PR -> 138
# Saquarema - RJ -> 94
# Votorantim - SP -> 86
# Catalão - GO -> 81
# Jandira - SP -> 93
# Maricá - RJ -> 115
# São João del Rei - MG -> 106
# Paracatu - MG  -> 81
# Macaé - RJ -> 246

# TOTAL: 1147

# Número de escolas por cidade
# Rio das Ostras - RJ -> 101
# Paranaguá - PR -> 133
# Saquarema - RJ -> 88
# Votorantim - SP -> 88
# Catalão - GO -> 70
# Jandira - SP -> 81
# Maricá - RJ -> 107
# São João del Rei - MG -> 65
# Paracatu - MG  -> 68
# Macaé - RJ -> 195

# TOTAL: 996

# URLs: 
# Para acessar quais cidades vamos considerar na busca: https://municipios.rankingdecompetitividade.org.br/
# Para acessar a lista de escolas na cidade: https://escolas.com.br/brasil/estado/cidade (tem paginação)


JSON = []
SCHOOLS = 0


def remove_accents(word):
    """Função auxiliar para remover acentos de palavras
    Usada para tratar nomes de cidades"""
    # Normalize to decompose combined characters
    nfkd_form = unicodedata.normalize('NFKD', word)
    # Filter out characters with non-spacing marks (accents)
    return ''.join([char for char in nfkd_form if not unicodedata.combining(char)])


def make_cities_request_orders(scheduler: Scheduler, url: str) -> None:
    """
    Função que faz parsing do conteúdo que vem do ranking de competitividade
    (https://municipios.rankingdecompetitividade.org.br/), formando as RequestOrders
    para o nível de cidades.

    Args:
        scheduler: ponteiro para o Scheduler
        url: URL relativa ao ranking de competitividade
    """
    response = requests.get(url, timeout=500)

    soup = BeautifulSoup(response.content, 'html.parser')

    section = soup.find('h2', string="Maiores Variações").find_parent('section')
    rows = section.find_all('tr')

    for row in rows[1:]:
        city = row.find('a').text.strip()  # Estrutura do texto -> 2. Paranaguá - PR
        city, state = city.split('. ')[1].split(' - ')

        ibge_base_url = "https://cidades.ibge.gov.br/brasil/"
        city_url = f'{ibge_base_url}/{state.lower()}/{city.lower().replace(" ", "-")}/panorama'

        new_request_order = RequestOrder(city_url, get_information_about_cit_on_ibge)
        scheduler.queue_request(new_request_order)

        base_url = 'https://escolas.com.br/brasil'
        city = remove_accents(city)
        city_url = f'{base_url}/{state.lower()}/{city.lower().replace(" ", "-")}'

        new_request_order = RequestOrder(city_url, make_schools_request_orders)
        scheduler.queue_request(new_request_order)


def get_information_about_cit_on_ibge(scheduler: Scheduler, url: str) -> None:
    
    response = requests.get(url, timeout=500)
    # soup = BeautifulSoup(response.content, 'html.parser')

    # if response.status_code != 200:
    #     print(f"Erro ao acessar a página. Status code: {response.status_code}")
    #     break

    # soup = BeautifulSoup(response.content, 'html.parser')

    # escolarizacao_tag = soup.find("td", class_="lista__nome", string="Taxa de escolarização de 6 a 14 anos de idade")
    # if escolarizacao_tag:
    #     taxa_escolarizacao_valor = escolarizacao_tag.find_next_sibling("td", class_="lista__valor")
    #     taxa_escolarizacao = taxa_escolarizacao_valor.find("span").text if taxa_escolarizacao_valor else "N/A"
    #     print("Taxa de escolarização:", taxa_escolarizacao + "%")


    # taxa_escolarizacao = soup.find('span', class_='escolarizacao') 
    # ideb_anos_iniciais = soup.find('span', class_='ideb')
    # ideb_anos_finais = soup.find('span', class_='ideb')

    # city_education_info = {
    #     "url": url,
    #     "taxa_escolarizacao": taxa_escolarizacao,
    #     "ideb_anos_iniciais": ideb_anos_iniciais,
    #     "ideb_anos_finais": ideb_anos_finais,
    # }

    # JSON.append({"cidade": city_education_info, "escolas": []})


def make_schools_request_orders(scheduler: Scheduler, url: str) -> None:
    """
    Função que, a partir de uma URL de cidade, prepara os RequestOrders para cada escola dessa cidade

    Args:
        scheduler: ponteiro para o Scheduler
        url: URL relativa a cidade
    """

    page = 1

    while True:
        search_url = f"{url}?pagina={page}"
        response = requests.get(search_url, timeout=500)

        if response.status_code != 200:
            print(f"Erro ao acessar a página para {search_url}. Status code: {response.status_code}")
            break

        soup = BeautifulSoup(response.content, 'html.parser')

        # Extração do número de escolas da página
        schools_urls = [i['href'] for i in soup.find_all('a', attrs={'data-link': 'listing-schools'})]

        if not schools_urls:
            break  # Se não houver mais escolas na página, interrompe a paginação

        for s_url in schools_urls:
            print(f"Escola: {s_url}")
            new_request_order = RequestOrder(s_url, get_information_about_school)
            scheduler.queue_request(new_request_order)

        print(f"Encontradas {len(schools_urls)} escolas na página {page} de {search_url}.")
        page += 1

        time.sleep(1)  # Intervalo para evitar sobrecarregar o servidor


def get_information_about_school(scheduler: Scheduler, url: str) -> None:
    """
    Função que, a partir de uma URL de escola, pega as informações da escola e, ao final,
    escreve no arquivo JSON

    Atributos a serem coletados sobre as escolas:
        - Nome da escola
        - Nível de adm (municipal, estadual, federal, particular)
        - Nível de educação (infantil, fundamental, médio, superior)
        - Possui EJA (booleano)?
        - Endereço

    Args:
        scheduler: ponteiro para o Scheduler
        url: URL relativa a escola
    """

    global SCHOOLS, JSON

    response = requests.get(url, timeout=500)

    if response.status_code != 200:
        print(f"Erro ao pegar informações da escola {url}")

    soup = BeautifulSoup(response.content, 'html.parser')

    # Coleta o nome da escola
    name_school = soup.find('h1').text.strip()
    # Coleta o nível de administração
    level = soup.find('span', class_='badge-warning')
    level_adm = level.text.strip() if level else 'Não informado'
    # Coleta o nível de educação
    levels_ed = soup.find_all('span', class_='badge-dark')
    levels_education = [span.text.strip() for span in levels_ed] if levels_ed else 'Não informado'
    # Coleta o endereço
    ad = soup.find('a', {'data-link': 'single-address-neighborhood'})
    address = ad.find_parent('p') if ad else None
    # Get text content from the <p> tag and remove the newlines and extra spaces
    address = ' '.join(address.stripped_strings) if address else 'Não informado'

    new_institution = {
        "nome": name_school,
        "level_adm": level_adm,
        "niveis_educacao": levels_education,
        "endereco": address,
        "url": url
    }

    SCHOOLS += 1
    time.sleep(1)
    JSON.append(new_institution)


def main():
    """Função principal"""
    scheduler = Scheduler()

    first_request_order = RequestOrder('https://municipios.rankingdecompetitividade.org.br', make_cities_request_orders)
    scheduler.queue_request(first_request_order)

    scheduler.run()

    print(f'Foram coletadas informações sobre {SCHOOLS} escolas')

    with open('escolas.json', 'w', encoding='utf-8') as file:
        json.dump(JSON, file, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
