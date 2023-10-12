from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from datetime import datetime

import pymongo
import re
import json
import os
import time

# Current Version
cv = "0.0.1"

# Current Working Directroy
cwd = os.getcwd()

# Number of SKATER PAGES on hockeystatcards.com
SKATER_PAGES = 11
# Number of GOALIE PAGES on hockeystatcards.com
GOALIE_PAGES = 1

# Error Handling
ERROR_CODE = '100'
with open(cwd + '/json/error-code-list.json', 'r') as json_file:
  ERROR_CODE_LIST = json.loads(json_file.read())

# Start date info
START_DATE = datetime(2023, 10, 10, 0, 0)


def get_nhl_day(today):
  # TODO FORMAT: dd-mm-yyyy
  return (today - START_DATE).days


def createSkater(obj, td_list):
  global ERROR_CODE
  global driver
  # FORMAT
  # Player(name), Team(logo), Position(Pos), Games Played(GP), Time On Ice(TOI),
  # Goals(G), Assists(A), Individual Expected Goals Created(ixG), Blocks(Blk), 
  # Penalties drawn - taken(Pen), Face-offs won - lost(FO), Expected Goals For(xGF), 
  # Expected Goals Against(xGA), Goals For(GF), Goals Against(GA), 
  # Game Score Average(GS Avg), Game Score Total(GS Total)
  with open(cwd + '/json/release-nhl/skater-table-labels.json', 'r') as json_file:
    labels = json.loads(json_file.read())

  for label in labels:
    if label == "TEAM":
       obj[label] = td_list.pop(0).find_element(By.XPATH, ".//img").get_attribute("src")
    else:
      obj[label] = td_list.pop(0).text
 

def createGoalie(obj, td_list):
  global ERROR_CODE

  with open(cwd + '/json/release-nhl/goalie-table-labels.json', 'r') as json_file:
    labels = json.loads(json_file.read())

  for label in labels:
    if label == "TEAM":
       obj[label] = td_list.pop(0).find_element(By.XPATH, ".//img").get_attribute("src")
    else:
      obj[label] = td_list.pop(0).text


def getSkatersFromSite(players, site):
  global ERROR_CODE
  # USING SELENIUM
  driver = webdriver.Chrome()
  driver.get(site)
  assert "HockeyStatCards.com" in driver.title
  
  # Select "Show traded players as one row"
  driver.find_element(By.XPATH, "//span[contains(@class, 'chakra-checkbox__control')]").click()

  page = 1  
  while (ERROR_CODE == '100'):  
    print(f"Processing skater webpage {page}...")
    # Allow 2 seconds to load page
    driver.implicitly_wait(2)

    # FIND ALL SKATERS
    tr_list = driver.find_elements(By.XPATH, f"//tr[contains(@class, 'css-0')]")
    # Remove first entry (website problem)
    tr_list.pop(0)

    # CREATE SKATER PROFILE
    for tr in tr_list:
        td_list = tr.find_elements(By.XPATH, ".//td")

        player_obj = {}

        createSkater(player_obj, td_list)

        # TODO Add players to a database with
        # Primary key: Player AND Team being unique
        # Until then, Sebastian Aho (NYI) will be skipped
        if player_obj and "PLAYER" in player_obj.keys():
            if player_obj["PLAYER"] == "Sebastian Aho" and not player_obj["POS"] == "C":
                print(f"skipping (fetch): {player_obj['PLAYER']} on {player_obj['TEAM']}")
            else:
                players[player_obj["PLAYER"]] = player_obj
    
    # CLICK NEXT NUMBER
    page += 1
    try:
        next_button = driver.find_element(By.XPATH, "//button[contains(text(),'>')]")
    
        next_button.click()
        if page == SKATER_PAGES + 1:
           raise Exception("Reached end of data")
    except:
       ERROR_CODE = '200'

  driver.close()
  ERROR_CODE = '100'



def getGoaliesFromSite(players, site):
  global ERROR_CODE
  # USING SELENIUM
  driver = webdriver.Chrome()
  driver.get(site)
  assert "HockeyStatCards.com" in driver.title

  # Select Position:Goalies in View Options
  select = Select(driver.find_element(By.XPATH, "//select[contains(@class, 'chakra-select css-16i4v3z')]"))
  select.select_by_visible_text('Goalies')

  # Select "Show traded players as one row"
  driver.find_element(By.XPATH, "//span[contains(@class, 'chakra-checkbox__control')]").click()

  page = 1  
  while (ERROR_CODE == '100'):
    print(f"Processing goalie webpage {page}...")
    # Allow 2 seconds to load page
    driver.implicitly_wait(2)
    # FIND ALL GOALIES
    tr_list = driver.find_elements(By.XPATH, f"//tr[contains(@class, 'css-0')]")
    # Remove first entry (website problem)
    tr_list.pop(0)

    # CREATE GOALIE PROFILE
    for tr in tr_list:
        td_list = tr.find_elements(By.XPATH, ".//td")

        player_obj = {}

        createGoalie(player_obj, td_list)

        if player_obj and "PLAYER" in player_obj.keys():
          players[player_obj["PLAYER"]] = player_obj

    # CLICK NEXT NUMBER
    page += 1
    try:
        next_button = driver.find_element(By.XPATH, "//button[contains(text(),'>')]")
      
        next_button.click()
        if page == GOALIE_PAGES + 1:
          raise Exception("Reached end of data")
    except:
        ERROR_CODE = '200'

  driver.close()
  ERROR_CODE = '100'


def makeDatabase(players):
  myclient = pymongo.MongoClient("mongodb://localhost:27017/")
  mydb = myclient["mydatabase"]
  # Return list of system's databases: 
  print(f"{myclient.list_database_names()}")


def main():
  global ERROR_CODE
  
  # Create Players database
  players = {}

  # Create Date (file name)
  date = datetime.today()
  date = '' + str(date.year) + '-' + str(date.month) + '-' + str(date.day)

  # Get skater data
  site = "https://www.hockeystatcards.com/all"
      
  getSkatersFromSite(players, site)
  getGoaliesFromSite(players, site)

  # Create Database
  #db = makeDatabase(players)
  ERROR_CODE = '200'

  with open(cwd + f'/json/release-nhl/2023-24/data/{date}.json', 'w') as json_file:
    json_file.write(json.dumps(players, indent = 4))
    print(f'''
    Player data has been fetch from https://www.hockeystatcards.com and written to ./json/release-nhl/2023-24/data/{date}.json
    Run `python src/release-nhl/{cv}/data-to-md.py` to update public/nhl23-24/ROSTERS.md file with the new data
    ''')

  print(f"Done!")
  
if __name__ == "__main__":
  main()

  