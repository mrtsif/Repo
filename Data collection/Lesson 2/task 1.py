import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/89.0.4389.128 Safari/537.36'}
inp = str(input('введите параметры поиска: ')).split(' ')
text = ''
for i in inp:
    if i != inp[-1]:
        text += i + '+'
    else:
        text += i
params = {'clusters': 'true',
          'enable_snippets': 'true',
          'salary': '',
          'st': 'searchVacancy',
          'text': text}


link = 'https://hh.ru'
response = requests.get(link + '/search/vacancy', params=params, headers=headers)
dom = bs(response.text, 'html.parser')
hh_list = dom.find_all('div', {'class': 'vacancy-serp-item__row vacancy-serp-item__row_header'})

def salary(x):
    salary_data = x.find('div', {'class': 'vacancy-serp-item__sidebar'})
    if salary_data is None:
        return None
    else:
        salary_data_nn = salary_data.getText().replace('\u202f', '').strip().split(' ')
        if len(salary_data_nn) == 3 and salary_data_nn[0] == 'от':
            min = int(salary_data_nn[1])
            max = None
            currency = salary_data_nn[-1]
            return {'min salary': min, 'max salary': max, 'currency': currency}
        elif len(salary_data_nn) == 3 and salary_data_nn[0] == 'до':
            min = None
            max = int(salary_data_nn[1])
            currency = salary_data_nn[-1]
            return {'min salary': min, 'max salary': max, 'currency': currency}
        elif len(salary_data_nn) == 4:
            min = int(salary_data_nn[0])
            max = int(salary_data_nn[2])
            currency = salary_data_nn[-1]
            return {'min salary': min, 'max salary': max, 'currency': currency}


vacancies = []




while True:
    for vacancy in hh_list:
        vacancy_data = {}
        vacancy_link = vacancy.find('a', {'class': 'bloko-link'})['href']
        vacancy_name = vacancy.find('a', {'class': 'bloko-link'}).text
        vacancy_salary = salary(vacancy)
        vacancy_data['name'] = vacancy_name
        vacancy_data['link'] = vacancy_link
        vacancy_data['salary'] = vacancy_salary
        vacancies.append(vacancy_data)

    next_page = dom.find('a', {'data-qa': "pager-next"}, {'class': 'bloko-button'})
    if next_page != None:
        next_link = next_page['href']
        response = requests.get(link + next_link, headers=headers)
        dom = bs(response.text, 'html.parser')
        hh_list = dom.find_all('div', {'class': 'vacancy-serp-item__row vacancy-serp-item__row_header'})
        continue
    else:
        break
pprint(vacancies)
