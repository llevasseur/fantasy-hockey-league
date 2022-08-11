import requests
from bs4 import BeautifulSoup
import json
import re
import sys

import fetch_player_data

def getSTeam(div_list, type):
    # type is either "home" or "away"
    
    for div in div_list:
        if div.get("class") == ['s-table-wrapper']:
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

            player_obj = {}

            for td in td_list:
                
    for div in div_list:
        print(div);

def main():
    players = {}

    website = input('Input statistics website: ')
    
    soup = fetch_player_data.getSoup(website);
    findPlayersFromSoup(players, soup)

    with open('../json/stat-player-data.json', 'w') as json_file:
        json_file.write(json.dumps(players, indent=4))
    
    print('''
    Player data has been fetched from '''+website+''' and written to /json/stat-player-data.json
    Run `python3 merge-data.py` to update the data in /json/merged-player-data.json
    ''')
if __name__ == "__main__":
    main()