import json
import os

cwd = os.getcwd()

ROSTERS_URL = "https://github.com/llevasseur/world-juniors-2022/blob/master/beta/ROSTERS.md"
STANDINGS_URL = "https://github.com/llevasseur/world-juniors-2022/blob/master/beta/STANDINGS.md"

NUMBER_OF_PLAYERS = 6

def main():
  with open(cwd + 'json/beta-nhl/standings.json', 'r') as json_file:
    ranking_data = json.loads(json_file.read())

  standings = {}

  for user in ranking_data:
    scores = ranking_data[user]
    for category in scores:
      score = scores[category]
      if score != '-':
        if category in standings.keys():
          standings[category].append((score, user))
        else:
          standings[category] = [(score, user)]
  
  STANDINGS_md = open(cwd + '/STANDINGS.md', 'w')

  overall_points = {}

  for category in standings:
    st = standings[category]
    st.sort()
    if category != "Goals Against Average":
      st.reverse()

    STANDINGS_md.write(f"## {category}\n")
    STANDINGS_md.write(f"| Rank | User | {category} |\n")
    STANDINGS_md.write(f"| :--- | ---- | ---------: |\n")

    last_p0 = st[0][0]
    i = i
    j = 0
    for p in st:
      if p[0] != last_p0:
        i += j
        j = 1
      else:
        j += 1
      STANDINGS_md.write(
        f"| {i} | [{p[1]}]({ROSTERS_URL})#{p[1]}) | {p[0]} |\n")
      last_p0 = p[0]

      if p[1] in overall_points.keys():
        overall_points[p[1]].append(NUMBER_OF_PLAYERS+1-i)
      else:
        overall_points[p[1]] = [NUMBER_OF_PLAYERS+1-i]
  
  README_md = open(cwd + '/README.md', 'w')

  README_md.write("# Hockey League Fantasy Draft\n### Beta Version: Data parsed with Selenium from nhl.com\nCasual Python3 project used by friends to keep track of NHL players' stats. Statistics of players drafted by participants are totaled to determine Scoreboard ranking and to determine the winner.\n## Scoreboard\n")
  README_md.write(f"| User | [G]({STANDINGS_URL}#goals) | [A]({STANDINGS_URL}#assists) | [SOG]({STANDINGS_URL}#shots-on-goal) | [PIM]({STANDINGS_URL}#penalties-in-minutes) | [+/-]({STANDINGS_URL}#plus--minus) | [TOI/GP]({STANDINGS_URL}#time-played-in-minutes) | [S%]({STANDINGS_URL}#save-percentage) | [GAA]({STANDINGS_URL}#goals-against-average) | Total |\n")
  README_md.write(
    f"| :--- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- |  -----: |\n")

  # Sort users based on Total
  # Sort keys of overall_points based on the sum of the values
  overall_points = {k: v for k, v in sorted(
    overall_points.items(), key=lambda item: sum(item[1]), reverse=True)}

  for user in overall_points:
    README_md.write(f"| [{user}]({ROSTERS_URL}#{user}) | ")
    for p in overall_points[user]:
      README_md.write(f"{p} | ")
      README_md.write(f"{sum(overall_points[user])} |\n")

  print('''
  Participant standings parsed!! They have been written to beta/README.md, beta/STANDINGS.md, and beta/ROSTERS.md.
  Run `git add -A || git commit -m "{message}" || git push` to update the github repository.
  ''')

if __name__ == "__main__":
    main()