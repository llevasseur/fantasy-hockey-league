import json
import os
import fetch_player_data

cwd = os.getcwd()

def handleTd(obj, td):
    cl = td.get('class')

    #print(cl)

def getSTeam(div_list, type):
    # type is either "home" or "away"
    team = 's-team--'+type
    print(team)
    for div in div_list:
        div_class = div.get("class")
        if div_class and team in div_class:
            return div

def findPlayersFromSoup(players, soup):
    div_list = soup.find_all('div')
    types = ["home", "away"]
    for type in types:
        s_team = getSTeam(div_list, type)

        if s_team:
            tr_list = s_team.find_all('tr')

        else:
            print('### S TEAM '+type+' NOT FOUND')
            return
        
        for tr in tr_list:
            td_list = tr.find_all('td')
            print(td_list)

            player_obj = {}

            for td in td_list:
                handleTd(player_obj, td)

def main():
    players = {}

    website = input('Input statistics website: ')
    
    soup = fetch_player_data.getSoup(website);
    findPlayersFromSoup(players, soup)

    with open(cwd + '/json/stat-player-data.json', 'w') as json_file:
        json_file.write(json.dumps(players, indent=4))
    
    print('''
    Player data has been fetched from '''+website+''' and written to /json/stat-player-data.json
    Run `python merge-data.py` to update the data in /json/merged-player-data.json
    ''')
if __name__ == "__main__":
    main()