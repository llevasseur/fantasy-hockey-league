import json

def main():
  with open('../json/draft-picks.json', 'r') as json_file:
    draft_data = json.loads(json_file.read())

  with open('../json/ep-player-data.json', 'r') as json_file:
    player_data = json.loads(json_file.read())

  team_data = {}
  manual_framework = {}

  for user in draft_data:
    for player in draft_data[user]:
      team = player_data[player]['team']
      if team not in team_data.keys():
        team_data[team] = {}
      team_data[team][player] = {"SOG": 0, "TPM": 0}
  

  print(json.dumps(team_data, indent=4))

if __name__ == "__main__":
  main()