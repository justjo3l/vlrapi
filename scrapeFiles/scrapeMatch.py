from distutils.fancy_getopt import wrap_text
from ssl import match_hostname
from selenium import webdriver
from bs4 import BeautifulSoup
import json
import re
import datetime

BASE = "https://www.vlr.gg"

# Tournament Name - WORKS
# Tournament URL - WORKS
# Match Name - WORKS
# Match Type - WORKS
# Streams - WORKS
# Vods - WORKS
# Team Scores - WORKS
# Team Names - WORKS
# Team URLs - WORKS

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--log-level=3")

driver = webdriver.Chrome(executable_path="chromedriver", options=options)

driver.set_window_size(1920, 1080)

counter = 0

def remove_indents(value):
    value = value.replace('\n', '')
    value = value.replace('\t', '')
    return value

while counter != 10:
    print("----" + str(counter) + "----")
    # Collects Content from Results Page
    driver.get("https://www.vlr.gg/matches/results")
    content = driver.page_source
    soup = BeautifulSoup(content, 'lxml')

    # Finds Match URL
    urls = soup.find_all('a', 'wf-module-item')
    match_url = BASE + urls[counter]['href']

    # Collects Content from Specific Match Page
    driver.get(match_url)
    content = driver.page_source
    soup = BeautifulSoup(content, 'lxml')


    final_dict = {}

    # Finds the tournament details
    tournament_details = soup.find('div', 'match-header-super')

    # Finds the tournament name
    tournament_name = tournament_details.div.a.div.div.text.strip()

    # Finds the tournament URL
    tournament_url = BASE + tournament_details.div.a['href']

    # Stores the tournament name and URL
    final_dict['tournament'] = {'name' : tournament_name, 'url' : tournament_url}

    # Finds the match name
    match_name = tournament_details.div.a.div.find_all('div')[1].text.strip()
    match_name = remove_indents(match_name)

    # Finds the match name
    match_type = soup.find_all('div', 'match-header-vs-note')[1].text.strip()

    # Stores the match name and match type
    final_dict['match'] = {"name" : match_name, "type" : match_type}

    # Finds the date and time
    date_time_info = soup.find('div', 'moment-tz-convert')
    date = datetime.datetime.strptime(date_time_info['data-utc-ts'].split()[0], "%Y-%m-%d").strftime("%d/%m/%Y")
    time = date_time_info['data-utc-ts'].split()[1]

    # Stores the date
    final_dict['date'] = date

    # Stores the time
    final_dict['time'] = time

    # Finds the streams
    stream_titles = soup.find_all('div', 'match-streams-btn-embed')
    stream_links = soup.find_all('a', 'match-streams-btn-external')
    streams = {}

    # Finds each stream individually
    for i in range(0, len(stream_titles)):
        if (i < len(stream_links) and stream_links[i]):
            streams['stream' + str(i+1)] = {'name' : stream_titles[i].text.strip(), 'url' : stream_links[i]['href']}
        else:
            if (stream_titles[i].parent['href']):
                streams['stream' + str(i+1)] = {'name' : stream_titles[i].text.strip(), 'url' : stream_titles[i].parent['href']}
            else:
                streams['stream' + str(i+1)] = {'name' : stream_titles[i].text.strip(), 'url' : 'N/A'}

    # Stores the streams
    final_dict['streams'] = streams

    # Finds the vods
    vod_title = soup.find('div', 'match-vods')
    vod_links = vod_title.find_all('a')
    vods = {}

    # Finds each vod individually
    for i in range(0, len(vod_links)):
        if (vod_links[i]):
            vods['vod' + str(i+1)] = {'name' : vod_links[i].text.strip(), 'url' : vod_links[i]['href']}

    # Stores the vods
    final_dict['vods'] = vods

    # Finds the team1 and team2 scores
    score = soup.find_all('div', 'match-header-vs-score')[1]
    team1_score = score.find_all('span')[0].text.strip()
    team2_score = score.find_all('span')[2].text.strip()

    # Stores the team1 and team2 scores
    final_dict['score'] = {"team1" : team1_score, "team2" : team2_score}

    # Finds the teams
    teams = soup.find_all('a', 'match-header-link')

    # Finds the team1 name and url
    team1_data = teams[0]
    team1 = {"name" : team1_data.find('div', 'wf-title-med').text.strip(), "url" : BASE + team1_data['href']}

    # Finds the team2 name and url
    team2_data = teams[1]
    team2 = {"name" : team2_data.find('div', 'wf-title-med').text.strip(), "url" : BASE + team2_data['href']}

    # Stores the team1 and team2 names and urls
    final_dict['teams'] = {"team1" : team1, "team2" : team2}

    # Finds the maps
    maps = {}
    map_select = soup.find_all('div', 'vm-stats-gamesnav-item')
    for i in range(1,len(map_select)):
        if remove_indents(map_select[i].text.strip()[1:len(map_select[i].text.strip())]) != 'N/A':
            map_page_url = BASE + map_select[i]['data-href']
            # Collects Content from each Map Page
            driver.get(map_page_url)
            content = driver.page_source
            soup = BeautifulSoup(content, 'lxml')
            maps['map' + str(i)] = remove_indents(map_select[i].text.strip()[1:len(map_select[i].text.strip())])

    print(maps)


    print(final_dict)
    counter += 1

driver.close()