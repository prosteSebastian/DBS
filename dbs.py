import requests
from bs4 import BeautifulSoup
import json

def gameDurCalc(game_id):
    api_url = 'https://lol.fandom.com/api.php'
    params = {
        'action': "query",
        'format': "json",
        'prop': "revisions",
        'titles': "V5 data:"+game_id,
        'rvprop': "content",
        'rvslots': "main"
    }

    response = requests.get(api_url, params=params)

    if response.status_code == 200:
        data = response.json()
        # print(data.pre)
        game_json_str = data['query']['pages'][list(data['query']['pages'])[0]]['revisions'][0]['slots']['main']['*']
        game_json = json.loads(game_json_str)

        #print(round(game_json['gameDuration']/60, 2))
        return round(game_json['gameDuration']/60, 2)


    else:
        print('Error:', response.status_code)


def gameDur(game_id):
    url = "https://lol.fandom.com/wiki/"
    url = url + game_id
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table', {'class': 'wikitable'})
    game_dur_id = table.find_all('td')[0].contents[0][:-1]
    return gameDurCalc(game_dur_id)


def main():

    teams = {"AST":1,"XL":2,"FNC":3,"G2":4,"MAD":5,"MSF":6,"RGE":7,"SK":8,"BDS":9,"VIT":10}
    users = {"Medic":62}

    url = "https://lol.fandom.com/wiki/LEC/2022_Season/Summer_Season"

    response = requests.get(url)

    soup = BeautifulSoup(response.content, 'html.parser')

    table = soup.find('table', {'id': 'md-table'})

    idT = 1
    idA = 1
    idB = 2
    for row in table.find_all('tr'):

        colls = row.find_all('td')
        len_row = len(colls)

        if len_row == 14:
            w = colls[0].text if colls[2].text[0]==1 else colls[1].text
            winner = "" + w
            #escape unicode from the team names
            winner = winner.replace("\u2060", "")
            game_id = colls[11].find('a')['href'].split('/')[-1]

            gamedur = gameDur(game_id)

            #print A
            teamA = colls[0].text.replace("\u2060", "")
            colls[0].text.replace("\u2060", "")
            #print(colls[0].text + ' vs ' + colls[1].text + ',caster: ' + colls[3].text + ' ,winner: ' + winner + ' ,mvp: ' + colls[13].text)
            print(f"insert into participation (id_participation, id_team, won) VALUES({idA},{teams[teamA]},{1 if teamA == winner else 0});")
            idA += 1
            #print B
            teamB = colls[1].text.replace("\u2060", "")
            colls[1].text.replace("\u2060", "")
            print(f"insert into participation (id_participation, id_team, won) VALUES({idA},{teams[teamB]},{1 if teamB == winner else 0});")
            print(f"insert into match(id_match, id_arena, id_person, player_id_person, id_participation, participation_id_participation, date_m, play_time) VALUES({idT},1,'{colls[3].text}','{colls[13].text}',{idA},{idB},'DATE'{gamedur});")
            idA += 1
            idB += 1
            idT+=1
if __name__ == "__main__":
    main()
