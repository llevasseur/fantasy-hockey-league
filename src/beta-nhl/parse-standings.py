import json
import os

cwd = os.getcwd()

NAME = "fantasy-hockey-league"
ROSTERS_URL = "https://github.com/llevasseur/"+NAME+"/blob/main/ROSTERS.md"
STANDINGS_URL = "https://github.com/llevasseur/"+NAME+"/blob/main/STANDINGS.md"

NUMBER_OF_PLAYERS = 6

def main():
  with open(cwd + '/json/beta-nhl/standings.json', 'r') as json_file:
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
    i = 1
    j = 0
    for p in st:
      if p[0] != last_p0:
        i += j
        j = 1
      else:
        j += 1
      STANDINGS_md.write(
          f"| {i} | [{p[1]}]({ROSTERS_URL}#{p[1]}) |  {p[0]} |\n")
      last_p0 = p[0]

      if p[1] in overall_points.keys():
        overall_points[p[1]].append(NUMBER_OF_PLAYERS+1-i)
      else:
        overall_points[p[1]] = [NUMBER_OF_PLAYERS+1-i]
  
  README_md = open(cwd + '/README.md', 'w')

  README_md.write("# Fantasy Hockey League\n### Beta Version: Data parsed with Selenium from nhl.com\nCasual Python3 project used by friends to keep track of NHL and WJC players' stats. Statistics of players drafted by participants are totaled to determine Scoreboard ranking and to determine the winner.\n## Scoreboard\n")
  README_md.write(f"| User | [G]({STANDINGS_URL}#user-content-goals) | [A]({STANDINGS_URL}#user-content-assists) | [SOG]({STANDINGS_URL}#user-content-shots-on-goal) | [PIM]({STANDINGS_URL}#user-content-penalties-in-minutes) | [+/-]({STANDINGS_URL}#user-content-plus--minus) | [TOI/GP]({STANDINGS_URL}#user-content-average-time-on-ice) | [S%]({STANDINGS_URL}#user-content-save-percentage) | [GAA]({STANDINGS_URL}#user-content-goals-against-average) | Total |\n")
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

  README_md.write("## Installation\nFork this repository to contribute. Commits will be analyzed before being added to the source code.\n## Usage\nParticipants can use this github to view stats, including the Scoreboard, Selected Roosters, and Standings in each category.\n\nTo update scores:\n1. Run the python script `python3 ./src/beta-nhl/fetch-player-data.py` to launch a Chrome instance using [Selenium](https://selenium-python.readthedocs.io/) for all Skaters and Goalies\n2. Run `python3 ./src/beta-nhl/data-to-md.py` to look up drafted player data in the newly created json database\n3. Run `python3 ./src/beta-nhl/parse-standings.py` to determine standings and the Scoreboard\n4. Add, commit, and push changes to this github repository.\n## Design Decisions: Beta\nFunctional Requirements:\n1. Request the [Selenium](https://selenium-python.readthedocs.io/) Chrome driver to extract all player data from each [nhl.com/stats](https://www.nhl.com/stats/skaters?reportType=season&seasonFrom=20222023&seasonTo=20222023&gameType=2&filter=gamesPlayed,gte,1&sort=points,goals,assists&page=0&pageSize=100) webpage with player statistics (page=[0,6]) and pageSize=100.\n<kbd>![nhl.com stats webpage example](/public/images/selenium_source.jpg)</kbd>\n\n2. Save data as a readable `json` database.\n\n<kbd>![json database entry example](/public/images/new_json_database.jpg)</kbd>\n\n3. Display the data in 3 locations: \n* ROSTERS.md: A visualizer for each participants drafted players' statistics. \n* STANDINGS.md: A visualizer for each participants overall totals versus each other. This determines rank. \n* README.md/Scoreboard: To make the scoreboard readily available for participants when they view this github repo, the Scoreboard is attached to this README. It is a visualizer for participant points based on rank for each category (Goals, Assists, etc). Participant points determine who's winning, or who wins, and is based off the number of players.\n<p align='center'><kbd><img src='/public/images/roster_example2.jpg' width='450' /></kbd><kbd><img src='/public/images/standings_example2.jpg' width='300' /></kbd><kbd><img src='/public/images/scoreboard_example2.jpg' width='500' /></kbd></p>\n\n## Contributing\nBug reports are welcome on Github at [Issues](https://github.com/llevasseur/world-juniors-2022/issues).\n## License\nThis project is available as open source under the terms of the [MIT License](https://opensource.org/licenses/MIT).\n## Future Work:\nAnticipated additions to this project include:\n1. Add metrics to each stat for each player and participant to detail change using red and green arrows and text.\n2. Plot statistics over games played using [Matplotlib](https://matplotlib.org/). Eventually, a model will be created to predict future performance statistics and outcome probability\n3. Facilitate roster changes including picking up and adding players to waivers, adding players that haven't been drafted, and trades.\n4. Customizable visualizers for each participant. Potentially would require its own website with a login and an SQL database.\n5. Automate all scripts to parse and update data at 12am pst using Make.")

  print('''
  Participant standings parsed!! They have been written to README.md, STANDINGS.md, and ROSTERS.md.
  Run `git add -A || git commit -m "{message}" || git push` to update the github repository.
  ''')

if __name__ == "__main__":
    main()