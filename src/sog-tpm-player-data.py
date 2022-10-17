# Set up for NHL.com League = NHL
# TODO Setup for League = WJC
import requests
from bs4 import BeautifulSoup
import re
import json
import os

cwd = os.getcwd()

def getSoup(url):
  response = requests.get(url)
  html = response.content
  
  return BeautifulSoup(html, 'html.parser')

def handleTd(obj, td):
    cl = td.get('class')

    #print(cl)

def getAppMain(soup):
    div_list = soup.find_all('div')
    for div in div_list:
        if div.get("class") == ['appMain']:
            return div

def findPlayersFromSoup(players, soup):
    print(soup)
    with open(cwd + "/src/test.html", "w", encoding="utf-8") as file:
        file.write(str(soup))
    app_main = getAppMain(soup)
    if app_main:
        tr_list = app_main.find_all('tr')
    else:
        print("### APP MAIN NOT FOUND")
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
    print(f"Provided url: {website}")
    
    soup = getSoup(website);
    findPlayersFromSoup(players, soup)

    with open(cwd + '/json/stat-player-data.json', 'w') as json_file:
        json_file.write(json.dumps(players, indent=4))
    
    print('''
    Player data has been fetched from '''+website+''' and written to /json/stat-player-data.json
    Run `python merge-data.py` to update the data in /json/merged-player-data.json
    ''')
if __name__ == "__main__":
    main()