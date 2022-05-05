from distutils.fancy_getopt import wrap_text
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import json
import datetime

def remove_indents(value):
    value = value.replace('\n', '')
    value = value.replace('\t', '')
    return value

def get_agent(value):
    value = value.strip()
    value = value.replace('/img/vlr/game/agents/', '')
    value = value.replace('.png', '')
    value = value.title()
    return value

def find_matches(limit):

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
    # Map Name - WORKS
    # Map Time Played - WORKS
    # Map Score - WORKS
    # Map Team Attack Scores - WORK
    # Map Team Defend Scores - WORK
    # Map Team Overtime Scores - WORK
    # Map Players - WORKS

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--log-level=3")

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    driver.set_window_size(1920, 1080)

    counter = 0
    page = int(0)
    final_list = []

    while counter != limit:
        # Collects Content from Results Page
        page = int(counter / 50)

        value = counter % 50

        if (page == 0):
            driver.get("https://www.vlr.gg/matches/results")
        else:
            driver.get(f"https://www.vlr.gg/matches/results/?page={page + 1}")

        content = driver.page_source
        soup = BeautifulSoup(content, 'lxml')

        # Finds Match URL
        urls = soup.find_all('a', 'wf-module-item')
        match_url = BASE + urls[value]['href']

        # Collects Content from Specific Match Page
        driver.get(match_url)
        content = driver.page_source
        soup = BeautifulSoup(content, 'lxml')


        temp_dict = {}

        # Finds the tournament details
        tournament_details = soup.find('div', 'match-header-super')

        # Finds the tournament name
        tournament_name = tournament_details.div.a.div.div.text.strip()

        # Finds the tournament URL
        tournament_url = BASE + tournament_details.div.a['href']

        # Stores the tournament name and URL
        temp_dict['tournament'] = {'name' : tournament_name, 'url' : tournament_url}

        # Finds the match name
        match_name = tournament_details.div.a.div.find_all('div')[1].text.strip()
        match_name = remove_indents(match_name)

        # Finds the match name
        match_type = soup.find_all('div', 'match-header-vs-note')[1].text.strip()

        # Stores the match name and match type
        temp_dict['match'] = {"name" : match_name, "type" : match_type}

        # Finds the date and time
        date_time_info = soup.find('div', 'moment-tz-convert')
        date = datetime.datetime.strptime(date_time_info['data-utc-ts'].split()[0], "%Y-%m-%d").strftime("%d/%m/%Y")
        time = date_time_info['data-utc-ts'].split()[1]

        # Stores the date
        temp_dict['date'] = date

        # Stores the time
        temp_dict['time'] = time

        # Finds the streams
        stream_titles = soup.find_all('div', 'match-streams-btn-embed')
        stream_links = soup.find_all('a', 'match-streams-btn-external') + soup.find_all('a', 'match-streams-btn')
        streams = []

        # Finds each stream individually
        for i in range(0, len(stream_titles)):
            if (i < len(stream_links) and stream_links[i]):
                streams.append({'name' : stream_titles[i].text.strip(), 'url' : stream_links[i]['href']})
            else:
                if (stream_links[i].parent['href']):
                    streams.append({'name' : stream_titles[i].text.strip(), 'url' : stream_links[i].parent['href']})
                else:
                    streams.append({'name' : stream_titles[i].text.strip(), 'url' : 'N/A'})

        # Stores the streams
        temp_dict['streams'] = streams

        # Finds the vods
        vod_title = soup.find('div', 'match-vods')
        vod_links = vod_title.find_all('a')
        vods = []

        # Finds each vod individually
        for i in range(0, len(vod_links)):
            if (vod_links[i]):
                vods.append({'name' : vod_links[i].text.strip(), 'url' : vod_links[i]['href']})

        # Stores the vods
        temp_dict['vods'] = vods

        # Finds the team1 and team2 scores
        score = soup.find_all('div', 'match-header-vs-score')[1]
        team1_score = score.find_all('span')[0].text.strip()
        team2_score = score.find_all('span')[2].text.strip()

        # Stores the team1 and team2 scores
        temp_dict['score'] = {"team1" : team1_score, "team2" : team2_score}

        # Finds the teams
        teams = soup.find_all('a', 'match-header-link')

        # Finds the team1 name and url
        team1_data = teams[0]
        team1 = {"name" : team1_data.find('div', 'wf-title-med').text.strip(), "url" : BASE + team1_data['href']}

        # Finds the team2 name and url
        team2_data = teams[1]
        team2 = {"name" : team2_data.find('div', 'wf-title-med').text.strip(), "url" : BASE + team2_data['href']}

        # Stores the team1 and team2 names and urls
        teams = []
        teams.append(team1)
        teams.append(team2)
        temp_dict['teams'] = teams

        solo = False

        # Finds the maps
        maps = []
        map_select = soup.find_all('div', 'vm-stats-gamesnav-item')
        if not map_select:
            map_select.append("placeholder")
            map_select.append("placeholder2")
            solo = True
        for i in range(1,len(map_select)):
            if solo or remove_indents(map_select[i].text.strip()[1:len(map_select[i].text.strip())]) != 'N/A':
                map = {}
                if not solo:
                    code = map_select[i]['data-game-id']

                # Collects Content from the Match Page
                driver.get(match_url)
                content = driver.page_source

                # Collects the Content for each Map
                if not solo:
                    soup = BeautifulSoup(content, 'lxml').find(lambda tag: tag.name == 'div' and tag.get('class') == ['vm-stats-game'] and tag.get('data-game-id') == code)
                else:
                    soup = BeautifulSoup(content, 'lxml').find('div', 'vm-stats-game')
                if soup:
                    map_name = remove_indents(soup.find('div', 'map').div.text.strip())
                    time_played = soup.find('div', 'map-duration').text.strip()

                    # Finds the map name
                    map['name'] = map_name

                    # Finds the time played
                    map['time_played'] = time_played
                    score = {}

                    # Finds the team1 map score
                    score['team1'] = soup.find_all('div', 'score')[0].text.strip()

                    # Finds the team2 map score
                    score['team2'] = soup.find_all('div', 'score')[1].text.strip()

                    # Finds the team1 map attack score
                    score['team1_attack'] = soup.find_all('span', 'mod-t')[0].text.strip()

                    # Finds the team2 map attack score
                    score['team2_attack'] = soup.find_all('span', 'mod-t')[1].text.strip()

                    # Checks if overtime happened
                    if (len(soup.find_all('span', 'mod-ot')) > 0):

                        # Finds the team1 map overtime score
                        score['team1_overtime'] = soup.find_all('span', 'mod-ot')[0].text.strip()

                        # Finds the team2 map overtime score
                        score['team2_overtime'] = soup.find_all('span', 'mod-ot')[1].text.strip()

                    # Finds the team1 map defend score
                    score['team1_defend'] = soup.find_all('span', 'mod-ct')[0].text.strip()

                    # Finds the team2 map defend score
                    score['team2_defend'] = soup.find_all('span', 'mod-ct')[1].text.strip()

                    # Stores the scores to the map
                    map['score'] = score

                    players = {}

                    team1 = []
                    team2 = []
                    player = {}

                    players1_table = soup.find_all('table', 'wf-table-inset')[0]
                    players1 = players1_table.find_all('tr')

                    for j in range(1, len(players1)):

                        # Stores player name
                        if (players1[j].find('td', 'mod-player').div.a.div.text):
                            player['name'] = players1[j].find('td', 'mod-player').div.a.div.text.strip()
                        else:
                            player['name'] = 'N/A'

                        # Stores player agent
                        if (players1[j].find('td', 'mod-agents').div.span.img):
                            player['agent'] = get_agent(players1[j].find('td', 'mod-agents').div.span.img['src'])
                        else:
                            player['agent'] = 'N/A'

                        # Stores player ACS
                        if (players1[j].find_all(lambda tag: tag.name == 'td' and tag.get('class') == ['mod-stat'])[0].span.find('span', 'mod-both').text):
                            player['ACS'] = players1[j].find_all(lambda tag: tag.name == 'td' and tag.get('class') == ['mod-stat'])[0].span.find('span', 'mod-both').text.strip()
                        else:
                            player['ACS'] = 'N/A'

                        # Stores player K
                        if (players1[j].find('td', 'mod-vlr-kills').span.find('span', 'mod-both').text):
                            player['K'] = players1[j].find('td', 'mod-vlr-kills').span.find('span', 'mod-both').text.strip()
                        else:
                            player['K'] = 'N/A'
                        
                        # Stores player D
                        if (players1[j].find('td', 'mod-vlr-deaths').span.find('span', 'mod-both').text):
                            player['D'] = players1[j].find('td', 'mod-vlr-deaths').span.find('span', 'mod-both').text.strip()
                        else:
                            player['D'] = 'N/A'
                        
                        # Stores player A
                        if (players1[j].find('td', 'mod-vlr-assists').span.find('span', 'mod-both').text):
                            player['A'] = players1[j].find('td', 'mod-vlr-assists').span.find('span', 'mod-both').text.strip()
                        else:
                            player['A'] = 'N/A'
                        
                        # Stores player KDA difference
                        if (players1[j].find('td', 'mod-kd-diff').span.find('span', 'mod-both').text):
                            player['KDA_difference'] = players1[j].find('td', 'mod-kd-diff').span.find('span', 'mod-both').text.strip()
                        else:
                            player['KDA_difference'] = 'N/A'

                        # Stores player KAST
                        if (players1[j].find_all(lambda tag: tag.name == 'td' and tag.get('class') == ['mod-stat'])[1].span.find('span', 'mod-both').text):
                            player['KAST'] = players1[j].find_all(lambda tag: tag.name == 'td' and tag.get('class') == ['mod-stat'])[1].span.find('span', 'mod-both').text.strip()
                        else:
                            player['KAST'] = 'N/A'

                        # Stores player ADR
                        if (players1[j].find_all(lambda tag: tag.name == 'td' and tag.get('class') == ['mod-stat'])[2].span.find('span', 'mod-both').text):
                            player['ADR'] = players1[j].find_all(lambda tag: tag.name == 'td' and tag.get('class') == ['mod-stat'])[2].span.find('span', 'mod-both').text.strip()
                        else:
                            player['ADR'] = 'N/A'

                        # Stores player HS%
                        if (players1[j].find_all(lambda tag: tag.name == 'td' and tag.get('class') == ['mod-stat'])[3].span.find('span', 'mod-both').text):
                            player['HS%'] = players1[j].find_all(lambda tag: tag.name == 'td' and tag.get('class') == ['mod-stat'])[3].span.find('span', 'mod-both').text.strip()
                        else:
                            player['HS%'] = 'N/A'

                        # Stores player FK
                        if (players1[j].find('td', 'mod-fb').span.find('span', 'mod-both').text):
                            player['FK'] = players1[j].find('td', 'mod-fb').span.find('span', 'mod-both').text.strip()
                        else:
                            player['FK'] = 'N/A'
                        
                        # Stores player FD
                        if (players1[j].find('td', 'mod-fd').span.find('span', 'mod-both').text):
                            player['FD'] = players1[j].find('td', 'mod-fd').span.find('span', 'mod-both').text.strip()
                        else:
                            player['FD'] = 'N/A'
                        
                        # Stores player FK difference
                        if (players1[j].find('td', 'mod-fk-diff').span.find('span', 'mod-both').text):
                            player['FK_difference'] = players1[j].find('td', 'mod-fk-diff').span.find('span', 'mod-both').text.strip()
                        else:
                            player['FK_difference'] = 'N/A'

                        # Stores player to team1
                        team1.append(player.copy())
                        
                    # Stores team1 to players
                    players['team1'] = team1

                    players2_table = soup.find_all('table', 'wf-table-inset')[1]
                    players2 = players2_table.find_all('tr')

                    for j in range(1, len(players2)):

                        # Stores player name
                        player['name'] = players2[j].find('td', 'mod-player').div.a.div.text.strip()

                        # Stores player agent
                        player['agent'] = get_agent(players2[j].find('td', 'mod-agents').div.span.img['src'])

                        # Stores player ACS
                        player['ACS'] = players2[j].find_all(lambda tag: tag.name == 'td' and tag.get('class') == ['mod-stat'])[0].span.find('span', 'mod-both').text.strip()
                        
                        # Stores player K
                        player['K'] = players2[j].find('td', 'mod-vlr-kills').span.find('span', 'mod-both').text.strip()
                        
                        # Stores player D
                        player['D'] = players2[j].find('td', 'mod-vlr-deaths').span.find('span', 'mod-both').text.strip()
                        
                        # Stores player A
                        player['A'] = players2[j].find('td', 'mod-vlr-assists').span.find('span', 'mod-both').text.strip()
                        
                        # Stores player KDA difference
                        player['KDA_difference'] = players2[j].find('td', 'mod-kd-diff').span.find('span', 'mod-both').text.strip()
                        
                        # Stores player KAST
                        player['KAST'] = players2[j].find_all(lambda tag: tag.name == 'td' and tag.get('class') == ['mod-stat'])[1].span.find('span', 'mod-both').text.strip()
                        
                        # Stores player ADR
                        player['ADR'] = players2[j].find_all(lambda tag: tag.name == 'td' and tag.get('class') == ['mod-stat'])[2].span.find('span', 'mod-both').text.strip()
                        
                        # Stores player HS%
                        player['HS%'] = players2[j].find_all(lambda tag: tag.name == 'td' and tag.get('class') == ['mod-stat'])[3].span.find('span', 'mod-both').text.strip()
                        
                        # Stores player FK
                        player['FK'] = players2[j].find('td', 'mod-fb').span.find('span', 'mod-both').text.strip()
                        
                        # Stores player FD
                        player['FD'] = players2[j].find('td', 'mod-fd').span.find('span', 'mod-both').text.strip()
                        
                        # Stores player FK Difference
                        player['FK_difference'] = players2[j].find('td', 'mod-fk-diff').span.find('span', 'mod-both').text.strip()
                        
                        # Stores player to team1
                        team2.append(player.copy())

                    # Stores team2 to players
                    players['team2'] = team2

                    # Stores the players to the map
                    map['players'] = players

                    # Stores the map to the maps
                    maps.append(map)

        # Stores the maps
        temp_dict['maps'] = maps

        final_list.append(temp_dict)


        print(temp_dict)
        counter += 1

    driver.close()

    matches = {}
    matches['data'] = final_list

    matches = json.dumps(matches)

    return json.loads(matches)