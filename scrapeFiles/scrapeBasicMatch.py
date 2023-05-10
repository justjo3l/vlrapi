import requests
from bs4 import BeautifulSoup
import json

def remove_indents(value):
    value = value.replace('\n', '')
    value = value.replace('\t', '')
    return value

def find_match(id):

    match = {}

    BASE = "https://www.vlr.gg"
    page = int(0)

    id = id - 1

    # Collects Content from Results Page
    page = int(id / 50)

    value = id % 50

    if (page == 0):
        r = requests.get("https://www.vlr.gg/matches/results")
    else:
        r = requests.get(f"https://www.vlr.gg/matches/results/?page={page + 1}")

    soup = BeautifulSoup(r.content, 'html.parser')

    matches_soup = soup.find_all('a', 'wf-module-item')

    match_soup = matches_soup[value]

    temp_dict = {}

    # Finds the tournament name
    tournament_name = match_soup.find('div', 'match-item-event').div.next_sibling.text.strip()
    tournament_name = remove_indents(tournament_name)

    # Stores the tournament name
    temp_dict['tournament'] = tournament_name

    # Finds the match name
    match_name = match_soup.find('div', 'match-item-event').div.text.strip()
    match_name = remove_indents(match_name)

    # Stores the match name and match type
    temp_dict['match'] = match_name

    team1 = {}
    team2 = {}

    # Finds the team1 and team2 names
    teams = match_soup.find_all('div', 'match-item-vs-team-name')
    team1['name'] = teams[0].text.strip()
    team2['name'] = teams[1].text.strip()

    # Finds the team1 and team2 scores
    score = match_soup.find_all('div', 'match-item-vs-team-score')
    team1['score'] = score[0].text.strip()
    team2['score'] = score[1].text.strip()

    # Stores the team1 and team2 names and scores
    temp_dict['teams'] = [team1, team2]

    print(temp_dict)

    match['data'] = temp_dict

    match = json.dumps(match)

    return json.loads(match)