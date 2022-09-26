import json  
import os

cwd = os.getcwd()

ROSTERS_URL = "https://github.com/llevasseur/world-juniors-2022/blob/master/ROSTERS.md"
STANDINGS_URL = "https://github.com/llevasseur/world-juniors-2022/blob/master/STANDINGS.md"

NUMBER_OF_PLAYERS=5

def main():
  with open(cwd + '/json/standings.json', 'r') as json_file:
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

  README_md = open(cwd + '/README.md', 'w')

  README_md.write("# World Junior Fantasy Draft\nCasual Python3 project used by friends to keep track of World Junior hockey players' stats. Statistics of players drafted by participants are totaled to determine Scoreboard ranking and to determine the winner.\n## Scoreboard\n")
  README_md.write(f"| User | [G]({STANDINGS_URL}#goals) | [A]({STANDINGS_URL}#assists) | [SOG]({STANDINGS_URL}#shots-on-goal) | [PIM]({STANDINGS_URL}#penalties-in-minutes) | [+/-]({STANDINGS_URL}#plus--minus) | [TPM]({STANDINGS_URL}#time-played-in-minutes) | [S%]({STANDINGS_URL}#save-percentage) | [GAA]({STANDINGS_URL}#goals-against-average) | Total |\n")
  README_md.write(f"| :--- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- |  -----: |\n")

  for user in overall_points:
    README_md.write(f"| [{user}]({ROSTERS_URL}#{user}) | ")
    for p in overall_points[user]:
      README_md.write(f"{p} | ")
    README_md.write(f"{sum(overall_points[user])} |\n")

  README_md.write("## Installation\nFork this repository to contribute. Commits will be analyzed before being added to the source code.\n## Usage\nParticipants can use this github to view stats, including the Scoreboard, Selected Roosters, and Standings in each category.\n\nTo update scores:\n1. Run the python script `python ./src/fetch-player-data.py`\n2. Write manual player data to `python ./src/write-manual-data.py`. Input ex: Firstname1 Lastname1,SOG,MM,SS, ...\n3. Run `python ./src/merge-data.py`\n4. Run `python ./src/data-to-md.py`\n5. Run `python ./src/parse-standings.py`\n6. Add, commit, and push changes to this github repository.\n## Design Decisions\nFunctional Requirements:\n1. Request a response from each webpage with player statistics (page=[1,3]). Extract the html from the response and pull out data using [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/).\n<kbd>>![elite prospects webpage example](/public/images/http_source.jpg)</kbd>\n2. \n## Contributing\nBug reports are welcome on Github at [Issues](https://github.com/llevasseur/world-juniors-2022/issues).\n## License\nThis project is available as open source under the terms of the [MIT License](https://opensource.org/licenses/MIT).\n## Future Work\nAnticipated additions to this project include:\n1. Automating write-manual-data.py to pull from a web scrapped website passed in. Game-specific data, including Shots on Goal (SOG) and Time Played in Minutes (TPM) can be parsed from player data. Example, [here](https://www.iihf.com/en/events/2022/wm20/gamecenter/statistics/37416/5-lat-vs-can).\n2. Displaying data using [Matplotlib](https://matplotlib.org/).\n3. Increasing scale of project to work for more leagues, like the [NHL](https://www.eliteprospects.com/league/nhl).\n4. Handling automated input for names with unfamiliar unicode, like `Topi Niemel\u00e4`.")

  print(cwd + "/public/images/http_source.jpg")

  

if __name__ == "__main__":
  main()