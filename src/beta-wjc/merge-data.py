import json 
import os
import datetime

cwd = os.getcwd()

START_DATE = datetime.datetime(2023, 12, 26, 0, 0)

def get_wjc_day(today):
  return (today - START_DATE).days

def readJSON(path):
  with open(path, 'r') as json_file:
    return json.loads(json_file.read())

def main():
  date = str(get_wjc_day(datetime.datetime.today()))

  ep_player_data = readJSON(cwd + "/json/beta-wjc/2023-24/ep-player-data.json")
  manual_player_data = readJSON(cwd + "/json/beta-wjc/2023-24/manual-player-data.json")

  for team in manual_player_data:
    players = manual_player_data[team]
    for name in players:
      try:
        stats = players[name]
        ep_player_data[name]['SOG'] = stats['SOG']
        ep_player_data[name]['TPM'] = stats['TPM']
      except:
        print("skipping (in merge) "+ name)
      

  with open(cwd + '/json/beta-wjc/2023-24/merged-player-data-day-'+date+'.json', 'w') as json_file:
    json_file.write(json.dumps(ep_player_data, indent=4))

  print(f'''
  Player data has been merged from /json/beta-wjc/2023-24/ep-player-data.json and /json/beta-wjc/2023-24/manual-player-data.json
  into /json/beta-wjc/2023-24/merged-player-data-day-{date}.json
  Run `python src/beta-wjc/data-to-md.py` to update the ROSTERS.md file with this new data
  ''')
  


if __name__ == "__main__":
  main()