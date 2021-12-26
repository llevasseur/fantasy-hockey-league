import requests
from bs4 import BeautifulSoup
import re
import json

def getSoup(url):
  response = requests.get(url)
  html = response.content
  
  return BeautifulSoup(html, 'html.parser')

def handleTd(obj, td):
  cl = td.get('class')

  ## Parse Name, href, and Position
  if cl == ['player']:
    a_list = td.find_all('a')
    for a in a_list:
      match = re.match('(.*)\s\((.*)\)', a.text)
      if match:
        name, pos = match.groups()
        if pos != "D": pos = 'F'
        obj["name"] = name
        obj["pos"] = pos
      else:
        obj["name"] = a.text
        obj["pos"] = "G"
      obj["href"] = a.get('href')

  ## Parse Team
  elif cl == ['team']:
    # if "name" in obj.keys(): print(f"Parsing team for {obj['name']}")
    a_list = td.find_all('a')
    for a in a_list:
      match = re.match('(.*) U20', a.text)
      if match:
        obj["team"] = match.group(1)
        # print(f"\t Found {match.group(1)}")

  # Parse Stats
  elif cl in [['g'], ['a'], ['pim'], ['pm'], ['gaa']]:
    obj[cl[0]] = td.text.strip()

  elif 'svp' in cl:
    obj['svp'] = td.text.strip()

def getInnerWrapper(soup):
  div_list = soup.find_all('div')
  for div in div_list:
    if div.get("class") == ['innerwrapper']:
      return div

def getPlayersFromSoup(players, soup):
  inner_wrapper = getInnerWrapper(soup)
  if inner_wrapper:
    tr_list = inner_wrapper.find_all('tr')
  else:
    print("### INNER WRAPPER NOT FOUND")
    return

  for tr in tr_list:
    td_list = tr.find_all('td')

    player_obj = {}

    for td in td_list:
      handleTd(player_obj, td)

    if player_obj and "name" in player_obj.keys():
      players[player_obj["name"]] = player_obj

def main():
  players = {}

  for i in range(1, 4):
    soup = getSoup("https://www.eliteprospects.com/league/wjc-20/stats/2020-2021?page="+str(i))
    getPlayersFromSoup(players, soup)

  with open('../json/ep-player-data.json', 'w') as json_file:
    json_file.write(json.dumps(players, indent=4))

  print('''
  Player data has been fetched from https://www.eliteprospects.com and written to /json/ep-player-data.json
  Run `python3 merge-data.py` to update the data in /json/merged-player-data.json
  ''')

if __name__ == "__main__":
  main()