from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup
import re
import json
import os
import time
cwd = os.getcwd()

def createSkater(obj, td_list):
  # Points-Rank, Name, Year, Team, Hand, Position, #GP, G, A, Points, +/-, PIM, P/Game, EVG, EVP, PPG, PPP, SHG, SHP, OTG, GWG, Shots, Shooting%, TOI/GP, FOW%. 
  labels = ["rank", "name", "year", "team", "hand", "pos", "gp", "g", "a", "p", "+/-", "pim", "p/g", "evg", "evp", "ppg", "ppp", "shg", "shp", "otg", "gwg", "sog", "sht%", "toi/gp", "fow%"]
  # Name, href, Position: Name, href in name <a>, Position
  # Stats: G, A, PIM, +/-
  index = 0
  while td_list:
    type = td_list.pop(0)

    # Parse Name, href
    if index == 1:
      a = type.find_element(By.XPATH, "//a")
      obj["name"] = type.text
      obj["href"] = a.get_attribute('href')

    # Parse Team
    elif index == 3:
      obj["team"] = type.text
    
    # Parse Position:
    elif index == 5:
      if type.text != "D":
        obj["pos"] = "F"
      else:
        obj["pos"] = "D"

    # Parse Stats:
    else:
      obj[labels[index]] = type.text

    index += 1 


def createGoalie(obj, td_list):
  # Rank, Name, Year, Team, Hand, #GP, #Games Started, W, L, Ties, OTL, Shots Against, Saves, Goals Allowed, Save%, GAA, TOI, Shutouts, Goals, Assists, Points, PIM
  labels = ["rank", "name", "year", "team", "hand", "gp", "gs", "w", "l", "t", "ot", "sa", "svs", "ga", "svp", "gaa", "toi", "so", "g", "a", "p", "pim", "pos"]

  index = 0
  while td_list:
    type = td_list.pop(0)

    # Parse Name, href
    
    if index == 1:
      a = type.find_element(By.XPATH, "//a")
      obj["name"] = type.text
      obj["href"] = a.get_attribute('href')
    
    # Parse Team
    elif index == 3:
      obj["team"] = type.text

    # Parse Stats:
    else:
      obj[labels[index]] = type.text
    
    index += 1
  obj["pos"] = "G"



def getSkatersFromSite(players, site):
  driver = webdriver.Chrome()
  driver.get(site)
  assert "NHL.com" in driver.title

  tr_list = driver.find_elements(By.XPATH, "//div[@class='rt-tr-group']")
  
  for tr in tr_list:
    sub_elem = tr.find_element(By.XPATH, ".//div[contains(@class, 'rt-tr -odd') or contains(@class, 'rt-tr -even')]")
    td_list = sub_elem.find_elements(By.XPATH, ".//div[contains(@class, 'rt-td')]")
    
    player_obj = {}

    createSkater(player_obj, td_list)

    if player_obj and "name" in player_obj.keys():
      players[player_obj["name"]] = player_obj

def getGoaliesFromSite(players, site):
  driver = webdriver.Chrome()
  driver.get(site)
  assert "NHL.com" in driver.title

  tr_list = driver.find_elements(By.XPATH, "//div[@class='rt-tr-group']")

  for tr in tr_list:
    sub_elem = tr.find_element(By.XPATH, ".//div[contains(@class, 'rt-tr -odd') or contains(@class, 'rt-tr -even')]")
    td_list = sub_elem.find_elements(By.XPATH, ".//div[contains(@class, 'rt-td')]")

    player_obj = {}

    createGoalie(player_obj, td_list)

    if player_obj and "name" in player_obj.keys():
      players[player_obj["name"]] = player_obj

def main():
  players = {}

  for i in range(0, 7):
    print(f"Processing skater webpage {i+1}...")
    # Skaters
    site = "https://www.nhl.com/stats/skaters?reportType=season&seasonFrom=20222023&seasonTo=20222023&gameType=2&filter=gamesPlayed,gte,1&page="+str(i)+"&pageSize=100"

    getSkatersFromSite(players, site)

  # Goalies
  print(f"Processing goalie webpage 1...")
  site = "https://www.nhl.com/stats/goalies?reportType=season&seasonFrom=20222023&seasonTo=20222023&gameType=2&filter=gamesPlayed,gte,1&page=0&pageSize=100"
  
  getGoaliesFromSite(players, site)

  print(f"Done!")

  with open(cwd + '/json/beta-nhl/ep-player-data.json', 'w') as json_file:
    json_file.write(json.dumps(players, indent=4))
    print('''
    Player data has been fetched from https://www.nhl.com and written to /json/beta-nhl/ep-player-data.json
    Run `python src/beta-nhl/write-manual-data.py` to add SOG and TPM to the data in /json/manual-player-data.json
    ''')

if __name__ == "__main__":
  main()