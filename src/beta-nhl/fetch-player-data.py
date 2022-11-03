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


def getPlayersFromSite(players, site):
  driver = webdriver.Chrome()
  driver.get(site)
  assert "NHL.com" in driver.title
  tr_list = driver.find_elements(By.XPATH, "//div[@class='rt-tr-group']")
  
  for tr in tr_list:
    sub_elem = tr.find_element(By.XPATH, ".//div[@class='rt-tr -odd']")
    td_list = sub_elem.find_elements(By.XPATH, ".//div[contains(@class, 'rt-td')]")
    
    
  #elem.clear()
  #elem.send_keys("pycon")
  #elem.send_keys(Keys.RETURN)
  #assert "No results found." not in driver.page_source
  #driver.close()
  return

def main():
  players = {}

  for i in range(0, 1):
    print(f"Processing skater webpage {i+1}...")
    # Skaters
    site = "https://www.nhl.com/stats/skaters?reportType=season&seasonFrom=20222023&seasonTo=20222023&gameType=2&filter=gamesPlayed,gte,1&page="+str(i)+"&pageSize=100"

    getPlayersFromSite(players, site)

  # Goalies
  print(f"Processing goalie webpage 1...")
  site = "https://www.nhl.com/stats/goalies?reportType=season&seasonFrom=20222023&seasonTo=20222023&gameType=2&filter=gamesPlayed,gte,1&page=0&pageSize=100"
  
  #getPlayersFromSite(players, site)

  print(f"Done!")

  with open(cwd + '/json/beta-nhl/ep-player-data.json', 'w') as json_file:
    json_file.write(json.dumps(players, indent=4))
    print('''
    Player data has been fetched from https://www.nhl.com and written to /json/beta-nhl/ep-player-data.json
    Run `python src/beta-nhl/write-manual-data.py` to add SOG and TPM to the data in /json/manual-player-data.json
    ''')

if __name__ == "__main__":
  main()