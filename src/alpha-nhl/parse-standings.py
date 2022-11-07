import json
import os

cwd = os.getcwd()

ROSTERS_URL = "https://github.com/llevasseur/world-juniors-2022/blob/master/ROSTERS.md"
STANDINGS_URL = "https://github.com/llevasseur/world-juniors-2022/blob/master/STANDINGS.md"

NUMBER_OF_PLAYERS = 6


def main():
    with open(cwd + '/json/alpha-nhl/standings.json', 'r') as json_file:
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

    README_md.write("# Hockey League Fantasy Draft\n### Alpha Version: Data parsed with BeautifulSoup from eliteprospects.com\nCasual Python3 project used by friends to keep track of NHL and WJC players' stats. Statistics of players drafted by participants are totaled to determine Scoreboard ranking and to determine the winner.\n## Scoreboard\n")
    README_md.write(f"| User | [G]({STANDINGS_URL}#user-content-goals) | [A]({STANDINGS_URL}#user-content-assists) | [SOG]({STANDINGS_URL}#user-content-shots-on-goal) | [PIM]({STANDINGS_URL}#user-content-penalties-in-minutes) | [+/-]({STANDINGS_URL}#user-content-plus--minus) | [TPM]({STANDINGS_URL}#user-content-time-played-in-minutes) | [S%]({STANDINGS_URL}#user-content-save-percentage) | [GAA]({STANDINGS_URL}#user-content-goals-against-average) | Total |\n")
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

    README_md.write("## Installation\nFork this repository to contribute. Commits will be analyzed before being added to the source code.\n## Usage\nParticipants can use this github to view stats, including the Scoreboard, Selected Roosters, and Standings in each category.\n\nTo update scores:\n1. Run the python script `python3 ./src/alpha-nhl/fetch-player-data.py`\n2. Write manual player data to `python3 ./src/alpha-nhl/write-manual-data.py`. Input ex: FirstInitial. Lastname, SOG, M, SS, ...\n3. Run `python3 ./src/alpha-nhl/merge-data.py`\n4. Run `python3 ./src/alpha-nhl/data-to-md.py`\n5. Run `python3 ./src/alpha-nhl/parse-standings.py`\n6. Add, commit, and push changes to this github repository.\n## Design Decisions: Alpha\nFunctional Requirements:\n1. Request a response from each [eliteprospect.com](https://www.eliteprospects.com/league/wjc-20/stats/2021-2022?page=1) webpage with player statistics (page=[1,9]).\n<kbd>![elite prospects webpage example](/public/images/http_source.jpg)</kbd>\n\nExtract the html from the response and pull out data using [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/), then save data as a `json` database.\n\n2. Some information is not provided on eliteprospect.com, including Shots on Goal and Time Played in Minutes. This information can be found on [iihf.com](https://www.iihf.com/en/events/2022/wm20/gamecenter/statistics/37416/5-lat-vs-can) or [nhl.com](https://www.nhl.com/gamecenter/bos-vs-nyr/2022/11/03/2022020161/recap/stats#game=2022020161,game_state=final,lock_state=final,game_tab=stats) game statistics summaries.\n<kbd>![iihf stats summary webpage example](/public/images/additional_source.jpg)</kbd>\n\nIn the Beta version, a [selenium](https://selenium-python.readthedocs.io/) web scraper will be used, however, it has not been perfected for the alpha version. In the mean time, player data is added manually to a separate `json` file. `write-manual-data.py` is a CLI API to do this easily, taking FirstInitial. Lastname, SOG, M, SS, ... , as input. Save data as a `json` database.\n\n3. Merge the fetched player database and the manual player database using `player_name` as the primary key. As some players have ascii characters not available on English keyboards, like `Tim St\u00fctzle`, a separate database has been created to determine player names based on the `FirstInitial. Lastname` input.\n\n4. Display the data in 3 locations: \n* ROSTERS.md: A visualizer for each participants drafted players' statistics. \n* STANDINGS.md: A visualizer for each participants overall totals versus each other. This determines rank. \n* README.md/Scoreboard: To make the scoreboard readily available for participants when they view this github repo, the Scoreboard is attached to this README. It is a visualizer for participant points based on rank for each category (Goals, Assists, etc). Participant points determine who's winning, or who wins, and is based off the number of players.\n<p align='center'><kbd><img src='/public/images/roster_example.jpg' width='450' /></kbd><kbd><img src='/public/images/standings_example.jpg' width='300' /></kbd><kbd><img src='/public/images/scoreboard_example.jpg' width='500' /></kbd></p>\n\n## Contributing\nBug reports are welcome on Github at [Issues](https://github.com/llevasseur/world-juniors-2022/issues).\n## License\nThis project is available as open source under the terms of the [MIT License](https://opensource.org/licenses/MIT).\n## Future Work: Beta Version\nAnticipated additions to this project include:\n1. Automating write-manual-data.py to pull from a web scrapped website passed in. Game-specific data, including Shots on Goal (SOG) and Time Played in Minutes (TPM) can be parsed from league player data. Example, [here](https://www.nhl.com/stats/skaters).\n2. Displaying data using [Matplotlib](https://matplotlib.org/).\n3. Facilitate roster changes including picking up and adding players to waivers, adding players that haven't been drafted, and trades.\n4. Customizable visualizers for each participant. Potentially would require a login and cloud database.")

    print('''
    Participant standings parsed!! They have been written to README.md, STANDINGS.md, and ROSTERS.md.
    Run `git add -A || git commit -m "{message}" || git push` to update the github repository.
    ''')

if __name__ == "__main__":
    main()
