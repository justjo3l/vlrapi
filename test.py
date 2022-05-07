import requests

BASE = "http://127.0.0.1:5000/"

response = requests.get(BASE + "matches/2")
print(response.json())
input()
response = requests.get(BASE + "matches/2/full")
print(response.json())