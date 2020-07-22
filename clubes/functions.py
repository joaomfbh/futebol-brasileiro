import requests
from bs4 import BeautifulSoup

def webpage_requests (url_site):
    response = requests.get(url_site)
    soup = BeautifulSoup(response.content, 'lxml')

    return soup


def remove_math_prefixes(dataframe, column_name):
    math_prefixes = ['bi','Bi','tri','Tri','tetra','Tetra','penta','Penta',
                     'hexa','Hexa','hepta','Hepta','octa','Octa','enea','Enea','deca','Deca']
    
    for i in math_prefixes:
        for j in range(dataframe.shape[0]):
            if i in dataframe[column_name][j]:
                dataframe.loc[j,column_name] = dataframe.loc[j,column_name].replace(i,'')
    
    return dataframe[column_name]