import json
import os

cwd = os.getcwd()

def write_to_data(team_data):
  # Make a json with updated reference to json
  with open(cwd + '/json/beta-wjc/2022-23/manual-player-data.json', 'w') as json_file:
    json_file.write(json.dumps(team_data, indent=4))
  return

def setupManualPlayerData(teams):
    
    with open(cwd + '/json/beta-wjc/2022-23/name-lookup-table.json', 'r') as json_file:
        print(json_file)
        lookup_teams = json.loads(json_file.read())

        for team in lookup_teams:
            team_obj = {}
            for player in lookup_teams[team]:
                team_obj[lookup_teams[team][player]] = {"SOG": 0, "TPM": 0}

            teams[team]=team_obj

    write_to_data(teams)


def main():
    teams = {"Canada": {}, "USA": {}, "Finland": {}, "Sweden": {}, "Czechia": {}, "Slovakia": {}, "Germany": {}, "Switzerland": {}, "Austria": {}, "Latvia": {}}

    setupManualPlayerData(teams)

    print(f'''
    Manual player data reset to SOG:0 and TPM:0 for all players in json/beta-wjc/2022-23/draft-picks.json
    ''')

if __name__ == "__main__":
    main()