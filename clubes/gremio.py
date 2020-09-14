import functions
import pandas as pd
import re
import hashlib
import requests
from bs4 import BeautifulSoup
import zipfile

try:
    def gremio_gather():
        with zipfile.ZipFile('offline_pages/offline_pages.zip','r') as zip_file:
            zip_file.extractall(path='offline_pages/')
            with open('offline_pages/gremio_26082020.html', 'rb') as file:
                page = file.read()
        
        # Get hash from local webpage
        page_text = BeautifulSoup(page,'lxml').text
        local_hash = hashlib.md5(page_text.encode('utf-8')).hexdigest()    

        # The variable store the hash from online webpage and soup
        website_content = functions.webpage_requests('https://gremio.net/titulos')

        if local_hash == website_content[0]:
            # Get countries from indexmundi website to remove the country names that live in conquests names
            country_content = functions.webpage_requests('https://www.indexmundi.com/pt/')
            country_soup = country_content[1]

            # Country names that not in indexmundi website
            country_names = []
            country_names.extend(['EUA','Estados Unidos da América','El Salvador','Holanda'])

            # Store country names in country_names list
            for i in country_soup.find('div', class_='c').find_all('a'):
                country_names.append(str(i.contents[0]))

            # Get soup from Gremio conquests page
            soup = website_content[1]

            # Get only necessary content, that means only the piece of conquests
            soup = soup.find('div', class_='col-xs-12 col-sm-12 col-md-12')
            
            # This pattern select the years with four digits and the names of conquests after the dash character
            pattern = re.compile(r"(\d{4})(\s\-\s)([\wÃãÁáÀàÂâÉéÈèÊêÍíÌìÕõÓóÒòÔôÚúÙùçÇ.ñ\"\-\s]+)")
            lista_conq = []

            for string in soup.strings:
                if len(re.findall(pattern, string)) > 0:
                    # Yeans in the index 0,2 and names in the index 0,0
                    lista_conq.append({'titulo':re.findall(pattern, string)[0][2],
                                       'ano_conquista':re.findall(pattern, string)[0][0]})

            # Store the content in a dataframe and make a copy to go to the clean step
            df = pd.DataFrame(lista_conq)
            df_clean = df.copy()

            '''
            Quality and structure issues:
            - Remove country names that live in the name of conquest
            - The math prefixes (bi, tri, tetra, etc) and some words lik ('Campeao do', 'Campeão da', 'Campeão invicto') must be removed to show the real name of conquest
            - Names that have "Campeão " must be renamed to "Campeoanto " plus the rest of name
            - In some cases, the word "Campeão" must be removed. Ex: "Campeão da Copa Libertadores da Améria" = "Copa Libertadores da Améria"
            '''

            #df_clean['titulo'] = df_clean.loc[:,'titulo'].str.replace(u'\xa0',u'')
            
            df_clean['titulo'] = functions.remove_math_prefixes(df_clean, 'titulo')

            # Convert the first letter of names that be in smallcase
            for i,j in enumerate(df_clean['titulo'].values):
                if j[0].islower():
                    df_clean.loc[i,'titulo'] = j[0].upper() + j[1:]

            # Remove country names that live in the name of conquest
            for i,j in enumerate(df_clean['titulo']):
                for k in country_names:
                    if j.split('-')[-1].strip() == k:
                        df_clean.loc[i,'titulo'] = j.split('-')[:-1][0]

            # This pattern select only the names that start with some expressions (words between |)
            pattern = r"^(Campeão da|Campeão do|Campeão invicto da|Campeão invicto do|campeão do)"

            # The selected names by pattern above will be replaced by blank text
            for i,j in enumerate(df_clean['titulo']):
                df_clean.loc[i,'titulo'] = re.sub(pattern,"",str(j) ,flags=re.IGNORECASE).strip()

            # Normalive the rest of names that not selected by functions above
            for i,j in enumerate(df_clean['titulo']):
                if df_clean.loc[i,'titulo'] == 'Campeão Copa Libertadores da América':
                    df_clean.loc[i,'titulo'] = 'Copa Libertadores da América'
                elif df_clean.loc[i,'titulo'] == 'Campeão Mundial Interclubes':
                    df_clean.loc[i,'titulo'] = 'Mundial Interclubes'
                elif df_clean.loc[i,'titulo'] == 'Cidade de Porto Alegre' or df_clean.loc[i,'titulo'] == 'Cidade':
                    df_clean.loc[i,'titulo'] = 'Campeonato da ' + j
                elif df_clean.loc[i,'titulo'] == 'Recopa Sul':
                    df_clean.loc[i,'titulo'] = 'Recopa Sul-Americana'
                else:
                    df_clean.loc[i,'titulo'] = df_clean.loc[i,'titulo'].replace('Campeão','Campeonato')

            functions.save_to_csv(df_clean, 'gremio')

            return df_clean
        else:
            raise Exception("The webpage changed and code must be reviewed.")
except Exception as e:
    print(e)