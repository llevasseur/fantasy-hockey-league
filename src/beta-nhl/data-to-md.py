import json
import re
import os

cwd = os.getcwd()

def validatePick(pick):
    KEYS = [
        "href",
        "team"
    ]

    for k in KEYS:
        if k not in pick.keys():
            print(f"\n### ERROR: Missing {k}")
            print()
            print(json.dumps(pick, indent=4))
            return False
        
    return True

def main():
  with open(cwd + '/json/beta-nhl/draft-picks.json', 'r') as json_file:
    draft_data = json.loads(json_file.read())

  with open(cwd + '/json/beta-nhl/ep-player-data.json') as json_file:
    player_data = json.loads(json_file.read())
    
  md_file = open(cwd + '/beta/ROSTERS.md', 'w')

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
    pim_total = 0
    pm_total = 0
    sog_total = 0
    toi_total = 0

    gaa_list =[]
    svp_list = []

    for pick in roster:

      try:

        if validatePick(player_data[pick]):

          href = player_data[pick]['href']
          pos = player_data[pick]['pos']
          team = player_data[pick]['team']
          print("test 1")

          if not pos:
            gaa = player_data[pick]['gaa']
            svp = player_data[pick]['svp']
            print("test 2")

            if re.match('[\d\.]+', gaa):
              gaa_list.append(float(gaa))
            else:
              gaa_list.append(100.0)
            if re.match('[\d\.]+', svp):
              svp_list.append(float(svp))
            else:
              svp_list.append(0.0)
        
            print("test 3")
            player_map[pos].append(
              f"| [{pick}]({href}) | {pos} | {team} | {svp} | {gaa} |\n")

          else:
            g = player_data[pick]['g']
            a = player_data[pick]['a']
            pim = player_data[pick]['pim']
            pm = player_data[pick]['+/-']
            sog = player_data[pick]['sog']
            toi = player_data[pick]['toi/gp']

            print("test 5")
            if re.match('\d+', g): g_total += int(g)
            if re.match('\d+', a): a_total += int(a)
            if re.match('\d+', pim): pim_total += int(pim)
            if re.match('\-?\d+', pm): pm_total += int(pm)

            print("test 6")
            sog_total += int(sog)
            toi_total = round(toi_total + toi, 2)
            print("test 1")
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
      "Average Time on Ice": round(toi_total, 2),
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
  Player data from /json/beta-nhl/ep-player-data.json has been used to update ROSTERS.md
  Run `python src/beta-nhl/parse-standings.py` to update the STANDINGS.md file with this new data
  ''')

if __name__ == "__main__":
  main()
