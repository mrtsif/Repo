# Скрапмнг данных об астероидах в промежуток времени
import json
from datetime import date
import requests

api_key = 'akPI76a1bgcKKsbaAs6rhSpa4WcdXp54bgxvrR7Z'
start_date = date(2012, 12, 21)
end_date = date(2012, 12, 21)
link = 'https://api.nasa.gov/neo/rest/v1/feed'
params = {'start_date': start_date, 'end_date': end_date, 'api_key': api_key}
response = requests.get(link, params=params)
j_data = response.json()
# pprint(j_data)
asteroids = []
count = j_data['element_count']
data = j_data['near_earth_objects']['2012-12-21']
for a in data:
    asteroids.append(a['name'])

summ = f'В промежуток с {start_date} по {end_date} на наибольшем сближении с землей находилось {count} астрероидов:' \
      f' {", ".join(asteroids)} '
print(summ)

with open('nasa', 'w', encoding='utf=8') as nasa:
    json.dump(summ, nasa)
