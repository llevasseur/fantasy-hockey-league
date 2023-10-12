from datetime import datetime

import json
import re
import os

# Current Version
cv = "0.0.1"

# Current Working Directroy
cwd = os.getcwd()

# Error Handling
ERROR_CODE = '100'
with open(cwd + '/json/error-code-list.json', 'r') as json_file:
  ERROR_CODE_LIST = json.loads(json_file.read())

# Start date info
START_DATE = datetime(2023, 10, 10, 0, 0)


def validatePick(pick):
    KEYS = [
        "PLAYER"
        "POS",
        "TEAM"
    ]

    for k in KEYS:
        if k not in pick.keys():
            print(f"\n### ERROR: Missing {k}")
            print()
            print(json.dumps(pick, indent=4))
            return False

    return True


def main():
  # Create Date (file name)
  date = datetime.today()
  date = '' + str(date.year) + '-' + str(date.month) + '-' + str(date.day)

  with open(cwd + '/json/release-nhl/2023-24/draft-picks.json', 'r') as json_file:
    draft_data = json.loads(json_file.read())

  with open(cwd + f'/json/release-nhl/2023-24/{date}.json') as json_file:
    player_data = json.loads(json_file.read())

  md_file = open(cwd + '/public/nhl23-24/ROSTERS.md', 'w')

  md_file.write("# Fantasy Rosters\n")

  ranking_data = {}

  for user in draft_data:
    roster = draft_data[user]
    player_map = {
      "F": [],
      "D": [],
      "G": []
    }

    g_total = 0
    a_total = 0
    pm_total = 0
    sog_total = 0
    toi_total = "0"

    gaa_list = []
    svp_list = []

    for pick in roster:
      
      try:
        if validatePick(player_data[pick]):
          pos = player_data[pick]['POS']
          team = player_data[pick]['TEAM']

          if pos == "G":
            print("TODO: Wait for dev to figure out goalie stats on hockeystatcards.com")
          else:
            g = player_data[pick]['G']
            a = player_data[pick]['A']
            pen = player_data[pick]['PEN']
            sog = player_data[pick]['sog']
            toi = player_data[pick]['toi/gp']

            if re.match('\d+', g): g_total += int(g)
            if re.match('\d+', a): a_total += int(a)
            if re.match('\d+', pim): pim_total += int(pim)
            pm_total = addPM(pm, pm_total)

            sog_total += int(sog)
            toi_total = addTOI(toi, toi_total)
            player_map[pos].append(
              f"| [{pick}]({href}) | {pos} | {team} | {g} | {a} | {sog} | {pim} | {pm} | {toi} |\n")
      except:
        print(f"skipping (data): {pick}")

    ranking_data[user] = {
      "Goals": g_total,
      "Assists": a_total,
      "Shots on Goal": sog_total,
      "Penalties in Minutes": pim_total,
      "Plus / Minus": pm_total,
      "Average Time on Ice": toi_total,
      "Save Percentage": max(svp_list) if svp_list else '-',
      "Goals Against Average": min(gaa_list) if svp_list else '-'
    }

    md_file.write(f"## {user}\n")
    md_file.write(f"| Player | Pos | Team | G | A | SOG | PIM | +/- | TOI/GP |\n")
    md_file.write(f"| :----- | --- | ---- | - | - | --- | --- | --- | ------ |\n")

    skaters = player_map["F"]
    skaters.extend(player_map["D"])

    for sk in skaters:
        md_file.write(sk)
    
    md_file.write(
        f"| **Totals** | | | {g_total} | {a_total} | {sog_total} | {pim_total} | {pm_total} | {toi_total} |\n")
    md_file.write(f"\n| Player | Pos | Team | S% | GAA |\n")
    md_file.write(f"| :----- | --- | ----| -- | --: |\n")

    goalies = player_map["G"]
    for g in goalies:
      md_file.write(g)
    
  with open(cwd + '/json/beta-nhl/standings.json', 'w') as json_file:
    json_file.write(json.dumps(ranking_data, indent=4))

  print('''
  Player data from /json/beta-nhl/ep-player-data.json has been used to update public/nhl22-23/ROSTERS.md
  Run `python src/beta-nhl/parse-standings.py` to update the public/nhl22-23/STANDINGS.md file with this new data
  ''')

if __name__ == "__main__":
  main()