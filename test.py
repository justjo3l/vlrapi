import requests

BASE = "http://127.0.0.1:5000/"

data = [{"team1": "Evil Geniuses", "team2": "Team Major Academy", "team1_score": 2, "team2_score": 1}, {"team1": "Cosmic Divide", "team2": "Synergy", "team1_score": 2, "team2_score": 1}, {"team1": "Moon Raccoons", "team2": "Shopify Rebellion", "team1_score": 2, "team2_score": 0}, {"team1": "Lenny Time", "team2": "Lycus Empire", "team1_score": 2, "team2_score": 1}]

for i in range(len(data)):
    response = requests.put(BASE + "match/" + str(i), data[i])
    print(response.json())

input()
response = requests.get(BASE + "match/6")
print(response.json())