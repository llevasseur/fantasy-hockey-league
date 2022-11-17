from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import requests
from bs4 import BeautifulSoup
import re
import json
import os
import datetime
import sql_module

from dotenv import load_dotenv

load_dotenv()
PW = os.getenv("SQL_PW")
DB = os.getenv("SQL_DB")

cwd = os.getcwd()


START_DATE = datetime.datetime(2022, 10, 11, 0, 0)

def get_nhl_day(today):
  return (today - START_DATE).days

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
      a = type.find_element(By.CSS_SELECTOR, "div > a")
      obj["name"] = type.text
      obj["href"] = a.get_attribute('href')

    # Parse Team
    elif index == 3:
      if len(type.text) > 3:
        obj["team"] = type.text[-3]
      else:
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
      a = type.find_element(By.CSS_SELECTOR, "div > a")
      obj["name"] = type.text
      obj["href"] = a.get_attribute('href')
    
    # Parse Team
    elif index == 3:
      if len(type.text) > 3:
        obj["team"] = type.text[-3]
      else:
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
      if player_obj["name"] == "Sebastian Aho" and not player_obj["team"] == "CAR":
            print(f"skipping (fetch): {player_obj['name']} on {player_obj['team']}")
      else:
        players[player_obj["name"]] = player_obj
  
  # Add skaters to database 
  """ entries = ""
  for player in players:
    entries += f"(S{player[]})" """



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

  date = str(get_nhl_day(datetime.datetime.today()))
  
  for i in range(0, 7):
    print(f"Processing skater webpage {i+1}...")
    # Skaters
    site = "https://www.nhl.com/stats/skaters?reportType=season&seasonFrom=20222023&seasonTo=20222023&gameType=2&filter=gamesPlayed,gte,1&page="+str(i)+"&pageSize=100"

    getSkatersFromSite(players, site)

  # Goalies
  print(f"Processing goalie webpage 1...")
  site = "https://www.nhl.com/stats/goalies?reportType=season&seasonFrom=20222023&seasonTo=20222023&gameType=2&filter=gamesPlayed,gte,1&page=0&pageSize=100"
  
  getGoaliesFromSite(players, site) 

  create_skater_table = """
  CREATE TABLE skater (
    skater_id  VARCHAR(4)  PRIMARY KEY,
    first_name VARCHAR(40) NOT NULL,
    last_name  VARCHAR(40) NOT NULL,
    href       VARCHAR(50) NOT NULL,
    year       VARCHAR(7)  NOT NULL,
    team       VARCHAR(3)  NOT NULL,
    hand       VARCHAR(1)  NOT NULL,
    pos        VARCHAR(1)  NOT NULL,
    gp         INT         NOT NULL,
    goals      INT         NOT NULL,
    assists    INT         NOT NULL,
    points     INT         NOT NULL,
    plus_minus        VARCHAR(4)  NOT NULL,
    pim        INT         NOT NULL,
    p_per_g        FLOAT       NOT NULL,
    evg        INT         NOT NULL,
    evp        INT         NOT NULL,
    ppg        INT         NOT NULL,
    ppp        INT         NOT NULL,
    shg        INT         NOT NULL,
    shp        INT         NOT NULL,
    otg        INT         NOT NULL,
    gwg        INT         NOT NULL,
    sht_perc       FLOAT       NOT NULL,
    toi_gp     VARCHAR(5)  NOT NULL,
    fow_perc       FLOAT  
  )
  """

  create_goalie_table = """
  CREATE TABLE goalie (
    goalie_id  VARCHAR(4)  PRIMARY KEY,
    first_name VARCHAR(40) NOT NULL,
    last_name  VARCHAR(40) NOT NULL,
    href       VARCHAR(50) NOT NULL,
    year       VARCHAR(7)  NOT NULL,
    team       VARCHAR(3)  NOT NULL,
    hand       VARCHAR(1)  NOT NULL,
    gp         INT         NOT NULL,
    gs         INT         NOT NULL,
    wins       INT         NOT NULL,
    loses      INT         NOT NULL,
    ties       INT                 ,
    ot         INT         NOT NULL,
    sa         INT         NOT NULL,
    svs        INT         NOT NULL,
    ga         INT         NOT NULL,
    svp        FLOAT       NOT NULL,
    gaa        FLOAT       NOT NULL,
    toi        VARCHAR(8)  NOT NULL,
    so         INT         NOT NULL,
    goals      INT         NOT NULL,
    assists    INT         NOT NULL,
    points     INT         NOT NULL,
    pim        INT         NOT NULL,
    pos        VARCHAR(1)  NOT NULL
  )
  """

  connection = sql_module.create_db_connection("localhost", "root", PW, DB)
  create_database_query = "CREATE DATABASE nhl_skaters"
  sql_module.execute_query(connection, create_skater_table)
  sql_module.execute_query(connection, create_goalie_table)

  print(f"Done!")
  
  with open(cwd + '/json/beta-nhl/2022-23/day-'+date+'.json', 'w') as json_file:
    json_file.write(json.dumps(players, indent=4))
    print(f'''
    Player data has been fetched from https://www.nhl.com and written to /json/beta-nhl/2022-23/{date}json
    Run `python src/beta-nhl/data-to-md.py` to update the ROSTERS.md file with this new data
    ''')

if __name__ == "__main__":
  main()