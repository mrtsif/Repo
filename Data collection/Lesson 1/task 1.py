# 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
import requests
import json

username = 'torvalds'
token = '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'
link = f'https://api.github.com/users/{username}/repos'
response = requests.get(link, auth=(username, token))
j_data = response.json()
i = 1
repos = []
for repo in j_data:
    repos.append(repo['name'])
    i += 1
repositories = f'{username} got {i} repositories ({", ".join(repos)})'
print(repositories)

with open('torvalds', 'w', encoding='utf=8') as torvalds:
    json.dump(repositories, torvalds)
