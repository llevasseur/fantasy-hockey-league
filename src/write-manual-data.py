import re
import json
import os

cwd = os.getcwd()

# Input format is
#     Firstname1 Lastname1,SOG,MM,SS, "Firstname2 Lastname2",SOG,MM,SS, ...
def time_to_float(x):
  return round((x/6) * 2) / 20

def write_to_data(manual_player_data):
  # Replace json with updated reference to json
  with open(cwd + '/json/manual-player-data.json', 'w') as json_file:
    json_file.write(json.dumps(manual_player_data, indent=4))
  return

def parse_manual_data(matches):
  # manual-player-data.json data for reference
  manual_player_data = {}
  with open(cwd + '/json/manual-player-data.json', 'r') as json_file:
    manual_player_data = json.loads(json_file.read())
    #print(f"\t### Manual Player Data: {manual_player_data}")

    # Pull data from list and update reference to json
    for id in matches:
      # id format is:
      #     Firstname Lastname,SOG,MM,SS
      name, SOG, min, sec = re.match('([\w|\s]*),([0-9]+),([0-9]{2}),([0-5][0-9]?)', id).groups()

      TPM = float(min) + time_to_float(float(sec))
    
      for country in manual_player_data:
        for player in manual_player_data[country]:
          #print(f"\t Player:{player}, Name:{name}")
          if player == name:
            #print(f"\tFound manual player data: {manual_player_data[country][player]["SOG"]}, {manual_player_data[country][player]["TPM"]}, {int(SOG)}, {TPM}")
            manual_player_data[country][player]["SOG"] += int(SOG)
            manual_player_data[country][player]["TPM"] += TPM
            break
  write_to_data(manual_player_data)
  return


def main():
  # Prompt user to input list
  data_list = input('Input, ex Firstname1 Lastname1,SOG,MM,SS, ...: ')

  matches = re.findall('[\w|\s]*,[0-9]+,[0-9]{2},[0-5][0-9]?', data_list)

  parse_manual_data(matches)

  print('''
  Manual player data has been updated and written to /json/manual-player-data.json
  ''')
        


if __name__ == "__main__":
  main()
    