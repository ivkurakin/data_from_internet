import requests
import json

repos_list = []
username = 'ivkurakin'
url = 'https://api.github.com/users/'+username+'/repos'
resp = requests.get(url)
if resp.status_code != 200:
    print("Error")
else:
    for part in resp.json():
        repos_list.append(part['name'])
print(repos_list)

with open(r'D:\repos.json', 'w') as f:
    json.dump(repos_list, f)

