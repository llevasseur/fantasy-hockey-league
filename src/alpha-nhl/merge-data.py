import json 
import os

cwd = os.getcwd()

def readJSON(path):
  with open(path, 'r') as json_file:
    return json.loads(json_file.read())

def main():
  ep_player_data = readJSON(cwd + "/json/alpha-nhl/ep-player-data.json")
  manual_player_data = readJSON(cwd + "/json/alpha-nhl/manual-player-data.json")

  for team in manual_player_data:
    players = manual_player_data[team]
    for name in players:
      try:
        stats = players[name]
        ep_player_data[name]['SOG'] = stats['SOG']
        ep_player_data[name]['TPM'] = stats['TPM']
      except:
        print("skipping (in merge) "+ name)
      

  with open(cwd + '/json/alpha-nhl/merged-player-data.json', 'w') as json_file:
    json_file.write(json.dumps(ep_player_data, indent=4))

  print('''
  Player data has been merged from /json/alpha-nhl/ep-player-data.json and /json/alpha-nhl/manual-player-data.json
  into /json/alpha-nhl/merged-player-data.json
  Run `python src/alpha-nhl/data-to-md.py` to update the ROSTERS.md file with this new data
  ''')
  


if __name__ == "__main__":
  main()