import functions
import pandas as pd
import re
import hashlib
import requests
from bs4 import BeautifulSoup
import zipfile

try:
    def chapecoense_gather():
        with zipfile.ZipFile('offline_pages/offline_pages.zip','r') as zip_file:
            zip_file.extractall(path='offline_pages/')
            with open('offline_pages/chapecoense_23092020.html', 'rb') as file:
                page = file.read()
        
        # Get hash from local webpage
        page_text = BeautifulSoup(page,'lxml').text
        local_hash = hashlib.md5(page_text.encode('utf-8')).hexdigest()    

        # The variable store the hash from online webpage and soup
        website_content = functions.webpage_requests('https://chapecoense.com/pt/titulos')

        if local_hash == website_content[0]:

            soup = website_content[1]

            # All data related with conquests are in 'item-titulo' div class
            chap_div = soup.find_all('div', class_='item-titulo')

            # Create empty lists to store the related data
            list_conquests = []
            list_years = []

            # Pattern to get years with four digits
            pattern = re.compile(r"(\d{4})")
            
            # Get conquests years
            for i in chap_div:
                for j in re.findall(pattern, i.p.text):
                    list_years.append(j)

            # Get conquests names
            for i in chap_div:
                for j in re.findall(pattern, i.p.text):
                    list_conquests.append(i.h2.text)

            # Create a dataframe and fill columns with years and names of conquests
            df = pd.DataFrame()
            df['titulo'] = list_conquests
            df['ano_conquista'] = list_years

            # Export data to csv
            functions.save_to_csv(df, 'chapecoense')

        else:
            raise Exception("The webpage changed and code must be reviewed.")
except Exception as e:
    print(e)

chapecoense_gather()