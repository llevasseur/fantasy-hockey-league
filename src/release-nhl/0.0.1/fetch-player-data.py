from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from datetime import datetime

import requests
from bs4 import BeautifulSoup
import re
import json
import os
import time


# Current Version
cv = "0.0.1"

# Current Working Directroy
cwd = os.getcwd()

driver = webdriver.Chrome()

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
  # Goals(G), First Assists(A1), Second Assists(A2), Assists(A), 
  # Individual Expected Goals Created(ixG), Blocks(Blk), Penalties drawn - taken(Pen),
  # Face-offs won - lost(FO), Expected Goals For(xGF), Expected Goals Against(xGA), 
  # Goals For(GF), Goals Against(GA), Game Score Average(GS Avg), Game Score Total(GS Total)
  with open(cwd + '/json/release-nhl/table-labels.json', 'r') as json_file:
    labels = json.loads(json_file.read())

  for label in labels:
    if label == "TOI":
       text = td_list.pop(0).get_text()
       print(f"{text}")
       obj[label] = text
    else:   
        obj[label] = td_list.pop(0).text 

def createGoalie(obj, td_list):
  global ERROR_CODE
  print(f"TODO: createGoalie(obj, td_list)")

def getSkatersFromSite(players, site):
  global ERROR_CODE
  global driver
  # USING SELENIUM
  
  driver.get(site)
  assert "Hockey Stat Cards" in driver.title

  page = 1  
  while (ERROR_CODE == '100'):  
    # Allow 2 seconds to load page
    driver.implicitly_wait(2)

    # FIND ALL SKATERS
    tr_list = driver.find_elements(By.CLASS_NAME, "all-skaters-row")

    # CREATE SKATER PROFILE
    for tr in tr_list:
        td_list = tr.find_elements(By.XPATH, ".//td")

        player_obj = {}

        createSkater(player_obj, td_list)

        # TODO Add players to a database with
        # Primary key: Player AND Team being unique
        # Until then, Sebastian Aho (NYI) will be skipped
        if player_obj and "Player" in player_obj.keys():
            if player_obj["Player"] == "Sebastian Aho" and not player_obj["Pos"] == "C":
                print(f"skipping (fetch): {player_obj['Player']} on {player_obj['Team']}")
            else:
                players[player_obj["Player"]] = player_obj
    
    # CLICK NEXT NUMBER
    page += 1
    try:
        next_button = driver.find_element(By.XPATH, f"//li[contains(@class, 'page-item') and contains(@title, '{page}')]")
    
        next_button.click()
        if page == 3:
           raise Exception("Blah")
    except:
       ERROR_CODE = '200'

  driver.close()

def getGoaliesFromSite(players, site):
  print(f"TODO: getGoaliesFromSite(players, site)")

def main():
  global ERROR_CODE
  
  # Create Players database
  players = {}

  # Create Date (file name)
  date = datetime.today()
  date = '' + str(date.year) + '-' + str(date.month) + '-' + str(date.day)

  # Get skater data
  site = "https://www.hockeystatcards.com/all-skaters"
  print(f"{site}")
      
  getSkatersFromSite(players, site)

  print(f"Done! {players}")
'''
    except NameError:
      error_num = ERROR_CODE_LIST.get(NameError)
      if error_num is not None:
        ERROR_CODE = error_num
        print(f"{ERROR_CODE}:{ERROR_CODE_LIST[ERROR_CODE]}.")
      else:
        ERROR_CODE = '999'
        print(f"{ERROR_CODE}:{ERROR_CODE_LIST[ERROR_CODE]}.")

      return

    except:
      print("unknown error without a name")
      ERROR_CODE = '999'
      print(f"{ERROR_CODE}:{ERROR_CODE_LIST[ERROR_CODE]}.")
      return
'''
  # if ERROR_CODE != '100' print error and return

  # Process each webpage for goalies, or use csv
  # if ERROR_CODE != '200' print error and return

  

'''
  with open(cwd + '/json/release-nhl/2023-24/{date}.json', 'w') as json_file:
    json_file.write(json.dumps(players, indent = 4))
    print(f''
    Player data has been fetch from https://www.hockeystatcards.com and written to /json/release-nhl/2023-24/{date}.json
    Run `python src/release-nhl/{cv}/data-to-md.py` to update public/nhl23-24/ROSTERS.md file with the new data
    '')

'''
    
  
if __name__ == "__main__":
  main()

  