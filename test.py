import requests

BASE = "http://127.0.0.1:5000/"

# for i in range(len(data)):
#     response = requests.put(BASE + "match/" + str(i), data[i])
#     print(response.json())
# input()

response = requests.get(BASE + "matches/1/full")
print(response.json())
input()
response = requests.get(BASE + "match/6/full")
print(response.json())