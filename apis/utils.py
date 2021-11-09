import requests
from bs4 import BeautifulSoup


def create_soup_object(data, from_type='url'):
    if from_type == 'url':
        page = requests.get(data)
        soup = BeautifulSoup(page.content, 'html.parser')
    elif from_type == 'html':
        soup = BeautifulSoup(data, 'html.parser')

    return soup


def get_max_page_in_category(soup):
    page_numbers = soup.find_all('a', class_='page-numbers')
    max_page = int(page_numbers[-2].text)

    return max_page
