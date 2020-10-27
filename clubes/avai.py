import functions
import pandas as pd
import requests
import re
import numpy as np
from bs4 import BeautifulSoup
import hashlib
import zipfile

try:
    def avai_gather():
        with zipfile.ZipFile('offline_pages/offline_pages.zip','r') as zip_file:
            zip_file.extractall(path='offline_pages/')
            with open('offline_pages/avai_27102020.htm', 'rb') as file:
                page = file.read()
        
        # Get hash from local webpage
        page_text = BeautifulSoup(page,'lxml').text
        local_hash = hashlib.md5(page_text.encode('utf-8')).hexdigest()    

        # The variable store the hash from online webpage and soup
        website_content = functions.webpage_requests('https://www.avai.com.br/novo/clube/historia/titulos/')

        if local_hash == website_content[0]:
            # Get soup from Gremio conquests page
            soup = website_content[1]
            
            # Get only the piece with conquests data
            soup = soup.find('div',class_='gdlr-item gdlr-main-content')

            # All expressions between | are replaced to ''
            pattern_cut = re.compile(r"– |TÍTULOS PROFISSIONAL|COMPETIÇÕES NACIONAIS|COMPETIÇÕES ESTADUAIS|COMPETIÇÕES CITADINAS|TÍTULOS – CATEGORIAS DE BASE|17 vezes|02 vezes|12 vezes|20 títulos|em|Campeão da|Campeão do")

            lst_conquests = []
            # All data is pure string, so i cut when iterator is equal to 'TÍTULOS – CATEGORIAS DE BASE', because only professional conquests interest us
            for i,j in enumerate(soup.strings):
                lst_conquests.append(re.sub(pattern_cut, '', j))
                if j == 'TÍTULOS – CATEGORIAS DE BASE':
                    break
            
            lst_conquests_final = []
            # Remove extra blank spaces and unicode character like new line(\n)
            for i in lst_conquests:
                i = i.strip()
                lst_conquests_final.append(i)
                if i == '\n' or i == '':
                    lst_conquests_final.remove(i)

            conquest = []
            year = []
            # The data in even index are the name of conquests while odd index are the year of this conquests
            for i,j in enumerate(lst_conquests_final):
                if i % 2 == 0:
                    conquest.append(j)
                else:
                    year.append(re.split(',| e ',j))

            # Create a dataframe and store the data between the columns
            df = pd.DataFrame()
            df['titulo'] = conquest
            df['ano_conquista'] = year

            # Create a backup off df
            df_clean = pd.DataFrame()

            # In the 'ano_conquista' column are many lists, so need to repeat the conquest name n times the len of the list
            # After that, the np.concatenate function flat the lists to object values
            lst_col = 'ano_conquista'
            pattern = r"(\d{4})"

            df_clean['titulo'] = np.repeat(df['titulo'].values, df[lst_col].str.len())
            df_clean['ano_conquista'] = np.concatenate([re.findall(pattern,i.strip()) for i in np.concatenate(df[lst_col])])

            '''
            Quality and structure issues:        
            - Convert 'ano_conquista' column to int
            - Remove conquest with the 'vice' in name (because only is a conquest only when in the first place, vice is equal to second place)
            - Campeonatos Regionais da Cidade de Florianópolis = Campeonato Regional da Cidade de Florianópolis
            - Trocar "Campeão" por "Campeoanto"
            - Remover "de Futebol"
            '''

            df_clean['ano_conquista'] = df_clean['ano_conquista'].astype(int)

            pattern_v = r'^vice'
            for i,j in enumerate(df_clean['titulo'].values):
                if re.findall(pattern_v,j,flags=re.IGNORECASE):
                    df_clean.drop(index=i, inplace=True)
    
                df_clean.reset_index(drop=True, inplace=True)

            pattern_f = r'de futebol'

            for i,j in enumerate(df_clean['titulo'].values):
                df_clean.loc[i,'titulo'] = re.sub(pattern_f,'',j,flags=re.IGNORECASE)
                if 'Campeão' in j:
                    df_clean.loc[i,'titulo'] = 'Campeonato' + df_clean.loc[i,'titulo'].split('Campeão')[1]
                if 'Campeonatos Regionais' in j:
                    df_clean.loc[i,'titulo'] = 'Campeonato Regional' + df_clean.loc[i,'titulo'].split('Campeonatos Regionais')[1]

            functions.save_to_csv(df_clean, 'avai')

            return df_clean
        else:
            raise Exception("The webpage changed and code must be reviewed.")
except Exception as e:
    print(e)