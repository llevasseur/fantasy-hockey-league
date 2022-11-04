import re
import json
import os

cwd = os.getcwd()

# Input format is
#     FirstInitial. Lastname, SOG, M, SS, ...
def time_to_float(x):
  return round(x/60, 2)

def write_to_data(manual_player_data):
  # Replace json with updated reference to json
  with open(cwd + '/json/alpha-nhl/manual-player-data.json', 'w') as json_file:
    json_file.write(json.dumps(manual_player_data, indent=4))
  return

def parse_manual_data(matches):
  # manual-player-data.json data for reference
  manual_player_data = {}
  with open(cwd + '/json/alpha-nhl/manual-player-data.json', 'r') as json_file:
    manual_player_data = json.loads(json_file.read())
    # name-lookup-table.json translates short hand name to reference name 
    with open(cwd + '/json/alpha-nhl/name-lookup-table.json', 'r') as json_file_2:
      name_lookup_table = json.loads(json_file_2.read())
      #print(f"\t### Manual Player Data: {manual_player_data}")

      # Pull data from list and update reference to json
      for id in matches:
        # id format is:
        #     FirstInitial. Lastname, SOG, M, SS, ...
        # name, SOG, min, sec = re.match('([\w|\s]*),([0-9]+),([0-9]{2}),([0-5][0-9]?)', id).groups()
        name, SOG, min, sec = re.match('[\s]*([\w|\s|.|\']*),[\s]*([0-9]+)[\s]*,[\s]*([0-9]{1,2})[\s]*,[\s]*([0-5][0-9]{0,1})[\s]*?', id).groups()
        name = name.rstrip()

        TPM = float(min) + time_to_float(float(sec))

        found = False
        for team in name_lookup_table:
          for player in name_lookup_table[team]:
            found = False
            if player.lower() == name.lower():
              name = name_lookup_table[team][player]
              #print(f"\t Player:{player}, Name:{name}")
              #print(f"\tFound manual player data: {manual_player_data[team][name]["SOG"]}, {manual_player_data[team][name]["TPM"]}, {int(SOG)}, {TPM}")
              manual_player_data[team][name]["SOG"] += int(SOG)
              manual_player_data[team][name]["TPM"] = round(manual_player_data[team][name]["TPM"] + TPM, 2)
              found = True
              break

          if found:
            break

  write_to_data(manual_player_data)
  return


def main():
  # Prompt user to input list
  data_list = input('Input, ex FirstInitial. Lastname, SOG, M, SS, ...: ')

  matches = re.findall('[\w|\s|.|\']*,[\s]*[0-9]+[\s]*,[\s]*[0-9]{1,2}[\s]*,[\s]*[0-5][0-9]{0,1}[\s]*?', data_list)

  parse_manual_data(matches)

  print('''
  Manual player data has been updated and written to /json/alpha-nhl/manual-player-data.json
  Run `python src/alpha-nhl/merge-data.py` to update the data in /json/alpha-nhl/manual-player-data.json
  ''')
        


if __name__ == "__main__":
  main()
    