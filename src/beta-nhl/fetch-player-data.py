from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup
import re
import json
import os

driver = webdriver.Firefox()
driver.get("http://www.python.org")
assert "Python" in driver.title
elem = driver.find_element(By.NAME, "q")
elem.clear()
elem.send_keys("pycon")
elem.send_keys(Keys.RETURN)
assert "No results found." not in driver.page_source
driver.close()

cwd = os.getcwd()

def getSoup(url):
  response = requests.get(url)
  html = response.content

  return BeautifulSoup(html, 'html.parser')

def getRoot(soup):
  div_list = soup.find_all('div')
  for div in div_list:
    if div.get("id") == "wrapper":
      return div

def getPlayersFromSoup(players, soup):
  root = getRoot(soup)
  if root:
    tr_list = root.find_all('div', {'class': 'rt-tr-group'})
    print(tr_list)
  return

def main():
  players = {}

  for i in range(0, 1):
    print(f"Processing skater webpage {i+1}...")
    # Skaters
    soup = getSoup("https://www.nhl.com/stats/skaters?reportType=season&seasonFrom=20222023&seasonTo=20222023&gameType=2&filter=gamesPlayed,gte,1&sort=points,goals,assists&page="+str(i)+"&pageSize=100")

    getPlayersFromSoup(players, soup)

  # Goalies
  print(f"Processing goalie webpage 1...")
  soup = getSoup("https://www.nhl.com/stats/goalies?reportType=season&seasonFrom=20222023&seasonTo=20222023&gameType=2&filter=gamesPlayed,gte,1&sort=wins,savePct&page=0&pageSize=100")
  
  #getPlayersFromSoup(players, soup)

  print(f"Done!")

  with open(cwd + '/json/beta-nhl/ep-player-data.json', 'w') as json_file:
    json_file.write(json.dumps(players, indent=4))
    print('''
    Player data has been fetched from https://www.nhl.com and written to /json/beta-nhl/ep-player-data.json
    Run `python src/beta-nhl/write-manual-data.py` to add SOG and TPM to the data in /json/manual-player-data.json
    ''')

if __name__ == "__main__":
  main()