import requests
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim
import time

# Função para extrair as cidades da URL fornecida
def pegar_nomes_cidades():
    url = 'https://municipios.rankingdecompetitividade.org.br/'
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Erro ao acessar a página. Status code: {response.status_code}")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Aqui está pegando todas cidades da página, mesmo fora do ranking
    th_elements = soup.find_all('th', class_='indicador')
    
    lista_cidades = []
    
    for th in th_elements:
        a_tag = th.find('a')
        if a_tag:
            cidade_text = a_tag.text.strip()
            lista_cidades.append(cidade_text)
    
    return lista_cidades[:1]

# Função para extrair cidade e estado
def extrair_cidade_estado(texto):
    partes = texto.split('. ')[1].split(' - ')
    cidade = partes[0].strip()
    estado = partes[1].strip()
    return cidade, estado

# Função para obter latitude e longitude usando geopy
def pegar_coordenadas(cidade):
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.geocode(cidade + ", Brasil")
    
    if location:
        return (location.latitude, location.longitude)
    else:
        return None

# Função para obter a previsão do tempo com base na latitude e longitude
def pegar_previsao_tempo(lat, lon):
    url = f"https://weather.com/weather/hourbyhour/l/{lat},{lon}"
    
    # url = 'https://weather.com/weather/hourbyhour/l/-23.5505,-46.6333'

    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Erro ao acessar a página de previsão do tempo. Status code: {response.status_code}")
        return None
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    previsoes = soup.find_all('span', class_='DetailsSummary--tempValue--jEiXE')
    
    if previsoes:
        return [prev.text.strip() for prev in previsoes]
    else:
        return None

# Main - Coordenando os passos
def main():
    cidades = pegar_nomes_cidades()
    print(cidades)
    
    if not cidades:
        print("Nenhuma cidade foi encontrada.")
        return
     
    for cidade_raw in cidades:
        cidade, estado = extrair_cidade_estado(cidade_raw)
        print(f"\nCidade: {cidade}, Estado: {estado}")
        
        coords = pegar_coordenadas(cidade)
        
        if not coords:
            print(f"Não foi possível obter as coordenadas para {cidade}.")
            continue
        
        print(f"Coordenadas de {cidade}: {coords}")
        
        previsao = pegar_previsao_tempo(coords[0], coords[1])
        print(previsao)
   
        time.sleep(2)

if __name__ == "__main__":
    main()
