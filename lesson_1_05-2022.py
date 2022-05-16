import requests
from pprint import pprint
url = 'https://api.github.com'
username = 'SergeyGoloushkin'
response = requests.get(f'{url}/users/{username}/repos')
with open('gh_repos_json', 'w') as file:
    j_data = response.json()
for repos in j_data:
   print(repos['name'])
