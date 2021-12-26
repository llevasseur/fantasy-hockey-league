import json

def readJSON(path):
  with open(path, 'r') as json_file:
    return json.loads(json_file.read())

def main():
  ep_player_data = readJSON("../json/ep-player-data.json")
  manual_player_data = readJSON("../json/manual-player-data.json")

  for team in manual_player_data:
    players = manual_player_data[team]
    for name in players:
      stats = players[name]
      ep_player_data[name]['SOG'] = stats['SOG']
      ep_player_data[name]['TPM'] = stats['TPM']

  with open('../json/merged-player-data.json', 'w') as json_file:
    json_file.write(json.dumps(ep_player_data, indent=4))

  print('''
  Player data has been merged from /json/ep-player-data.json and /json/manual-player-data.json
  into /json/merged-player-data.json
  Run `python3 data-to-md.py` to update the ROSTERS.md file with this new data
  ''')
  


if __name__ == "__main__":
  main()