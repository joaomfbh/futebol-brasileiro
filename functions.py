import requests
from bs4 import BeautifulSoup

def webpage_requests (url_site):
    response = requests.get(url_site)
    soup = BeautifulSoup(response.content, 'lxml')

    return soup