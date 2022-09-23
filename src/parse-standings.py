import json  

ROSTERS_URL = "https://github.com/llevasseur/world-juniors-2022/blob/master/ROSTERS.md"
STANDINGS_URL = "https://github.com/llevasseur/world-juniors-2022/blob/master/STANDINGS.md"

NUMBER_OF_PLAYERS=5

def main():
  with open('../json/standings.json', 'r') as json_file:
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

  STANDINGS_md = open('../STANDINGS.md', 'w')

  overall_points = {}

  for category in standings:
    st = standings[category]
    st.sort()
    if category != "Goals Against Average": st.reverse()

    STANDINGS_md.write(f"## {category}\n")
    STANDINGS_md.write(f"| Rank | User | {category} |\n")
    STANDINGS_md.write(f"| :--- | ---- | ---------: |\n")

    last_p0 = st[0][0]
    i = 1
    j = 0
    for p in st:
      if p[0] != last_p0:
        i += j
        j = 1
      else:
        j += 1
      STANDINGS_md.write(f"| {i} | [{p[1]}]({ROSTERS_URL}#{p[1]}) |  {p[0]} |\n")
      last_p0 = p[0]

      if p[1] in overall_points.keys():
        overall_points[p[1]].append(NUMBER_OF_PLAYERS+1-i)
      else:
        overall_points[p[1]] = [NUMBER_OF_PLAYERS+1-i]

  README_md = open('../README.md', 'w')

  README_md.write("# World Junior Fantasy Draft\nCasual Python3 project used by friends to keep track of World Junior hockey players' stats. Statistics of players drafted by participants are totaled to determine Scoreboard ranking and to determine the winner.\n## Scoreboard\n")
  README_md.write(f"| User | [G]({STANDINGS_URL}#goals) | [A]({STANDINGS_URL}#assists) | SOG | [PIM]({STANDINGS_URL}#penalties-in-minutes) | [+/-]({STANDINGS_URL}#plus--minus) | TPM | [S%]({STANDINGS_URL}#save-percentage) | [GAA]({STANDINGS_URL}#goals-against-average) | Total |\n")
  README_md.write(f"| :--- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- |  -----: |\n")

  for user in overall_points:
    README_md.write(f"| [{user}]({ROSTERS_URL}#{user}) | ")
    for p in overall_points[user]:
      README_md.write(f"{p} | ")
    README_md.write(f"{sum(overall_points[user])} |\n")

  README_md.write("## Installation\nRequest to fork this repository to contribute. Commits will be analyzed before added to the source code.\n## Usage\nParticipants can use this github to view stats, including the Scoreboard, Selected Roosters, and Standings in each category.\n\nTo update scores:\n\t1. Run the python script `python ./src/fetch-player-data.py`\n\t2. Write manual player data to `python ./src/write-manual-data.py`. Input ex: Firstname1 Lastname1,SOG,MM,SS, ...\n\t3. Run `python ./src/merge-data.py`\n\t4. Run `python ./src/data-to-md.py`\n\t5. Run `python ./src/parse-standings.py`\n\t6. Add, commit, and push changes to this github repository.\n## Design Decisions\n[Todo]\n## Contributing\nBug reports are welcome on Github at [Issues](link here).\n## License\nThis gem is available as open source under the terms of the [MIT License](https://opensource.org/licenses/MIT).\n")

  

if __name__ == "__main__":
  main()