import pandas as pd
import requests
from bs4 import BeautifulSoup

def cruzeiro_gather():
    try:
        # Url from Cruzeiro conquests page
        url = 'https://www.cruzeiro.com.br/conquistas'
        response = requests.get(url)
        page = response.content

        # Pass the page to Beautiful soup method to start page scraping
        soup = BeautifulSoup(page, 'lxml')

        # Create empty lists to get data
        nome_titulos = []
        anos_titulos = []
        anos_outros_titulos = []

        # Get the number total of conquests from 'TÍTULOS INTERNACIONAIS' and 'TÍTULOS NACIONAIS'
        total_titulos = len(soup.find_all('div', class_='card card-person card-conq')) 

        for i in range(total_titulos):
            # Iterate to get the names of conquests
            nome_titulos.append(soup.find_all('a', 'card-title valign-wrapper')[i].get_text().strip())

            # Iterate to get year of conquests
            anos_titulos.append(soup.find_all('div', class_='card-content')[i].get_text().replace('\n',''))

        
        # Get the category 'OUTROS TÍTULOS'
        nomes_outros_titulos = soup.find_all('h4')

        # Get the years from 'OUTROS TÍTULOS'
        for i in range(len(nomes_outros_titulos)):
            anos_outros_titulos.append(soup.find_all('p', class_='flow-text')[i].get_text().replace('\n','').strip())
    
        # Need to repeat the name of conquests according to years of these conquests
        for i in range(len(nomes_outros_titulos)):
            for j in range(len(anos_outros_titulos[i].split(', '))):
                nome_titulos.append(nomes_outros_titulos[i].get_text())

        # Store the years from 'OUTROS TÍTULOS' in the years of all conquests list
        for i in range(len(anos_outros_titulos)):
            anos_titulos.extend(anos_outros_titulos[i].split(', '))

        if len(nome_titulos) == len(anos_titulos):
            
            df = pd.DataFrame()
            df['titulo'] = nome_titulos
            df['ano_conquista'] = anos_titulos
            df['ano_conquista'] = df['ano_conquista'].astype(int)

            return df
        else:
            raise Exception("The name of conquests don't match with the years of conquests. Code update required!")
    except Exception as e:
            print(e)

