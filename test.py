import requests

BASE = "http://127.0.0.1:5000/"

response = requests.get(BASE + "match/1/full")

# response = requests.get(BASE + "stats/Sayf/TL/1190/FK")
print(response.json())