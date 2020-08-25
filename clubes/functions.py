import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import re

def webpage_requests (url_site):
    content_r = [0,0]
    response = requests.get(url_site)
    
    content_r[0] = len(response.content)
    content_r[1] = BeautifulSoup(response.content, 'lxml')

    return content_r

def remove_math_prefixes(dataframe, column_name):
    pattern = r"^(bi|tri|tetra|penta|hexa|hepta|octa|enea|deca)"
    
    for i,j in enumerate(dataframe[column_name]):
        dataframe.loc[i,column_name] = re.sub(pattern, "", j, flags=re.IGNORECASE)

    return dataframe[column_name]

def save_to_csv(dataframe, file_name):
    if os.path.exists('files'):
        dataframe.to_csv('files/'+file_name+'.csv', sep=',', encoding='iso-8859-1', index=False)
    else:
        os.mkdir('files')
        dataframe.to_csv('files/'+file_name+'.csv', sep=',', encoding='iso-8859-1', index=False)