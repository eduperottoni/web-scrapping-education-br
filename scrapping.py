import requests
from bs4 import BeautifulSoup
import time

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

# Função para extrair as cidades da URL fornecida
def get_cities() -> list[tuple[str, str]]:
    # Isso deve ser descomentado após o desenvolvimento
    # url = 'https://municipios.rankingdecompetitividade.org.br/'
    # response = requests.get(url)

    # Isso deve ser apagado após o desenvolvimento
    # with open('rankingcompetitividade.html', 'wb') as file:
    #     file.write(response.content)

    # Isso deve ser descomentado após o desenvolvimento
    # if response.status_code != 200:
    #     print(f"Erro ao acessar a página. Status code: {response.status_code}")
    #     return []

    # Isso deve ser modificado após o desenvolvimento
    with open('rankingcompetitividade.html', 'rb') as file:
        soup = BeautifulSoup(file.read(), 'html.parser')

    section = soup.find('h2', string="Maiores Variações").find_parent('section')
    rows = section.find_all('tr')

    cities: list[tuple[str, str]] = []
    for row in rows[1:]:  # Skip the header row
        city = row.find('a').text.strip()  # Estrutura do texto -> 2. Paranaguá - PR
        city, state = city.split('. ')[1].split(' - ')
        cities.append((city, state))

    return cities


def create_request_orders_for_cities(cities: list[tuple[str, str]]) -> str:
    # TODO: Criar RequestOrders para as cidades
    ...

def get_request_orders_for_schools(cities: list[tuple[str, str]]) -> str:
    # TODO: criar RequestOrders para as escolas
    url = 'https://escolas.com.br/brasil/sc/florianopolis'
    # response = requests.get(url)

    # with open('floripa-outro-site.html', 'wb') as file:
    #     file.write(response.content)

    with open('floripa-escolas-com.html', 'rb') as file:
        soup = BeautifulSoup(file.read(), 'html.parser')


# Main - Coordenando os passos
def main():
    cidades = get_cities()
    print(cidades)
    create_request_orders_for_cities(cidades)

    if not cidades:
        print("Nenhuma cidade foi encontrada.")
        return
 
if __name__ == "__main__":
    main()
