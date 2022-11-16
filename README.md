# Fantasy Hockey League
### Beta Version: Data parsed with Selenium from nhl.com
Casual Python3 project used by friends to keep track of NHL and WJC players stats. Statistics of players drafted by participants are totaled to determine Scoreboard ranking and to determine the winner.

 Find me on Mastodon! <a rel="me" href="https://techhub.social/@leevonlevasseur">Mastodon</a>
## Scoreboard
| User | [G](https://github.com/llevasseur/fantasy-hockey-league/blob/main/STANDINGS.md#user-content-goals) | [A](https://github.com/llevasseur/fantasy-hockey-league/blob/main/STANDINGS.md#user-content-assists) | [SOG](https://github.com/llevasseur/fantasy-hockey-league/blob/main/STANDINGS.md#user-content-shots-on-goal) | [PIM](https://github.com/llevasseur/fantasy-hockey-league/blob/main/STANDINGS.md#user-content-penalties-in-minutes) | [+/-](https://github.com/llevasseur/fantasy-hockey-league/blob/main/STANDINGS.md#user-content-plus--minus) | [TOI/GP](https://github.com/llevasseur/fantasy-hockey-league/blob/main/STANDINGS.md#user-content-average-time-on-ice) | [S%](https://github.com/llevasseur/fantasy-hockey-league/blob/main/STANDINGS.md#user-content-save-percentage) | [GAA](https://github.com/llevasseur/fantasy-hockey-league/blob/main/STANDINGS.md#user-content-goals-against-average) | Total |
| :--- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- |  -----: |
| [Alasdair](https://github.com/llevasseur/fantasy-hockey-league/blob/main/ROSTERS.md#Alasdair) | 6 | 6 | 5 | 5 | 6 | 3 | 4 | 4 | 39 |
| [John](https://github.com/llevasseur/fantasy-hockey-league/blob/main/ROSTERS.md#John) | 2 | 4 | 4 | 2 | 4 | 6 | 5 | 5 | 32 |
| [Timo](https://github.com/llevasseur/fantasy-hockey-league/blob/main/ROSTERS.md#Timo) | 5 | 5 | 6 | 2 | 5 | 4 | 1 | 1 | 29 |
| [Liam](https://github.com/llevasseur/fantasy-hockey-league/blob/main/ROSTERS.md#Liam) | 1 | 1 | 2 | 6 | 2 | 5 | 6 | 6 | 29 |
| [Carsten](https://github.com/llevasseur/fantasy-hockey-league/blob/main/ROSTERS.md#Carsten) | 4 | 2 | 3 | 4 | 1 | 2 | 3 | 2 | 21 |
| [Leevon](https://github.com/llevasseur/fantasy-hockey-league/blob/main/ROSTERS.md#Leevon) | 3 | 3 | 1 | 3 | 3 | 1 | 2 | 3 | 19 |
## Installation
Fork this repository to contribute. Commits will be analyzed before being added to the source code.
## Usage
Participants can use this github to view stats, including the Scoreboard, Selected Roosters, and Standings in each category.

To update scores:
1. Run the python script `python3 ./src/beta-nhl/fetch-player-data.py` to launch a Chrome instance using [Selenium](https://selenium-python.readthedocs.io/) for all Skaters and Goalies
2. Run `python3 ./src/beta-nhl/data-to-md.py` to look up drafted player data in the newly created json database
3. Run `python3 ./src/beta-nhl/parse-standings.py` to determine standings and the Scoreboard
4. Add, commit, and push changes to this github repository.
## Design Decisions: Beta
Functional Requirements:
1. Request the [Selenium](https://selenium-python.readthedocs.io/) Chrome driver to extract all player data from each [nhl.com/stats](https://www.nhl.com/stats/skaters?reportType=season&seasonFrom=20222023&seasonTo=20222023&gameType=2&filter=gamesPlayed,gte,1&sort=points,goals,assists&page=0&pageSize=100) webpage with player statistics (page=[0,6]) and pageSize=100.
<kbd>![nhl.com stats webpage example](/public/images/selenium_source.jpg)</kbd>

2. Save data as a readable `json` database.

<kbd>![json database entry example](/public/images/new_json_database.jpg)</kbd>

3. Display the data in 3 locations: 
* ROSTERS.md: A visualizer for each participants drafted players' statistics. 
* STANDINGS.md: A visualizer for each participants overall totals versus each other. This determines rank. 
* README.md/Scoreboard: To make the scoreboard readily available for participants when they view this github repo, the Scoreboard is attached to this README. It is a visualizer for participant points based on rank for each category (Goals, Assists, etc). Participant points determine who's winning, or who wins, and is based off the number of players.
<p align='center'><kbd><img src='/public/images/roster_example.jpg' width='450' /></kbd><kbd><img src='/public/images/standings_example.jpg' width='300' /></kbd><kbd><img src='/public/images/scoreboard_example.jpg' width='500' /></kbd></p>

## Contributing
Bug reports are welcome on Github at [Issues](https://github.com/llevasseur/world-juniors-2022/issues).
## License
This project is available as open source under the terms of the [MIT License](https://opensource.org/licenses/MIT).
## Future Work:
Anticipated additions to this project include:
1. Add metrics to each stat for each player and participant to detail change using red and green arrows and text.
2. Plot statistics over games played using [Matplotlib](https://matplotlib.org/). Eventually, a model will be created to predict future performance statistics and outcome probability
3. Facilitate roster changes including picking up and adding players to waivers, adding players that haven't been drafted, and trades.
4. Customizable visualizers for each participant. Potentially would require its own website with a login and an SQL database.
5. Automate all scripts to parse and update data at 12am pst using Make.