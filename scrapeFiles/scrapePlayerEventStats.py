import requests
from bs4 import BeautifulSoup
import json

def scrape(url, name, code, stat_code):
    print("Scraping for " + name)
    r = requests.get(url)

    soup = BeautifulSoup(r.content, 'html.parser')
    stats_table = soup.find('table', attrs={'class': 'mod-stats'})

    headers = dict()

    for id, header in enumerate(stats_table.find_all('th')):
        headers[header.text.strip()] = id
        
    print(headers)

    for id, row in enumerate(stats_table.find_all('tr')):
        if (row.find('td', attrs={'class': 'mod-player'}) == None):
            continue
        elif (row.find('td', attrs={'class': 'mod-player'}).text.strip() == f"{name}\n{code}"):
            return row.find_all('td')[headers[stat_code]].text.strip()

def find_stats(player_name, team_code, event_id, stat_code):
    url = f"https://www.vlr.gg/event/stats/{event_id}/"

    stat = scrape(url, player_name, team_code, stat_code)

    stats = {}
    stats[stat_code] = stat
    stats = json.dumps(stats)
    return json.loads(stats)
