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

def getPlayersFromSoup(players, soup):
    return

def main():
  players = {}

  for i in range(0, 7):
    print(f"Processing webpage {i}...")
    soup = getSoup("https://www.nhl.com/stats/skaters?reportType=season&seasonFrom=20222023&seasonTo=20222023&gameType=2&filter=gamesPlayed,gte,1&sort=points,goals,assists&page="+str(i)+"&pageSize=100")

    getPlayersFromSoup(players, soup)

  print(f"Done!")

  print(f"{cwd} /json/beta-nhl/ep-player-data.json")

  with open(cwd + '/json/beta-nhl/ep-player-data.json', 'w') as json_file:
    json_file.write(json.dumps(players, indent=4))
    print('''
    Player data has been fetched from https://www.nhl.com and written to /json/beta-nhl/ep-player-data.json
    Run `python src/beta-nhlwrite-manual-data.py` to add SOG and TPM to the data in /json/manual-player-data.json
    ''')

if __name__ == "__main__":
  main()