import requests
from bs4 import BeautifulSoup
import json

keywords = ["Django", "Flask"]

url = "https://hh.ru/search/vacancy?area=1&area=2&st=searchVacancy&text=Python"

def get_vacancies(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    vacancies = []
    for vacancy in soup.find_all('div', class_='vacancy-serp-item'):
        vacancy_data = {}
        vacancy_data['title'] = vacancy.find('a', class_='bloko-link')['data-qa']
        vacancy_data['company'] = vacancy.find('a', class_='bloko-link bloko-link_secondary')['data-qa']
        vacancy_data['city'] = vacancy.find('span', class_='vacancy-serp-item__meta-info').text
        vacancy_data['salary'] = vacancy.find('div', class_='vacancy-serp-item__compensation')
        vacancy_data['link'] = vacancy.find('a', class_='bloko-link')['href']

        vacancies.append(vacancy_data)

    return vacancies

def filter_vacancies(vacancies, keywords):
    filtered_vacancies = []
    for vacancy in vacancies:
        description_url = "https://hh.ru" + vacancy['link']
        description_response = requests.get(description_url)
        description_soup = BeautifulSoup(description_response.text, 'html.parser')
        description = description_soup.find('div', class_='vacancy-description')

        if all(keyword in description.text for keyword in keywords):
            filtered_vacancies.append(vacancy)

    return filtered_vacancies
vacancies = get_vacancies(url)
filtered_vacancies = filter_vacancies(vacancies, keywords)

with open('vacancies.json', 'w', encoding='utf-8') as file:
    json.dump(filtered_vacancies, file, ensure_ascii=False, indent=4)
