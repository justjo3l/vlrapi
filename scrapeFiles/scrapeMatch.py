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
# Team1 Score - WORKS
# Team2 Score - WORKS

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--log-level=3")

driver = webdriver.Chrome(executable_path="chromedriver", options=options)

driver.set_window_size(1920, 1080)

counter = 0

while counter != 5:
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
    match_name = match_name.replace('\n', '')
    match_name = match_name.replace('\t', '')

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
    final_dict['score'] = {"team1_score" : team1_score, "team2_score" : team2_score}

    print(final_dict)
    counter += 1

driver.close()