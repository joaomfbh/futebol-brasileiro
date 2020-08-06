import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

def webpage_requests (url_site):
    content_r = [0,0]
    response = requests.get(url_site)
    
    content_r[0] = len(response.content)
    content_r[1] = BeautifulSoup(response.content, 'lxml')

    return content_r

def remove_math_prefixes(dataframe, column_name):
    math_prefixes = ['bi','Bi','tri','Tri','tetra','Tetra','penta','Penta',
                     'hexa','Hexa','hepta','Hepta','octa','Octa','enea','Enea','deca','Deca']
    
    for i in math_prefixes:
        for j in range(dataframe.shape[0]):
            if i in dataframe[column_name][j]:
                dataframe.loc[j,column_name] = dataframe.loc[j,column_name].replace(i,'')
    
    return dataframe[column_name]

def save_to_csv(dataframe, file_name):
    if os.path.exists('files'):
        dataframe.to_csv('files/'+file_name+'.csv', sep=',', encoding='iso-8859-1', index=False)
    else:
        os.mkdir('files')
        dataframe.to_csv('files/'+file_name+'.csv', sep=',', encoding='iso-8859-1', index=False)