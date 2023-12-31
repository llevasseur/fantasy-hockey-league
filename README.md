# Fantasy Hockey League
### Beta Version: Data parsed with BeautifulSoup from eliteprospects.com
Casual Python3 project used by friends to keep track of NHL and WJC players' stats. Statistics of players drafted by participants are totaled to determine Scoreboard ranking and to determine the winner.
## Scoreboard
| User | [G](https://github.com/llevasseur/fantasy-hockey-league/blob/main/STANDINGS.md#user-content-goals) | [A](https://github.com/llevasseur/fantasy-hockey-league/blob/main/STANDINGS.md#user-content-assists) | [SOG](https://github.com/llevasseur/fantasy-hockey-league/blob/main/STANDINGS.md#user-content-shots-on-goal) | [PIM](https://github.com/llevasseur/fantasy-hockey-league/blob/main/STANDINGS.md#user-content-penalties-in-minutes) | [+/-](https://github.com/llevasseur/fantasy-hockey-league/blob/main/STANDINGS.md#user-content-plus--minus) | [TPM](https://github.com/llevasseur/fantasy-hockey-league/blob/main/STANDINGS.md#user-content-time-played-in-minutes) | [S%](https://github.com/llevasseur/fantasy-hockey-league/blob/main/STANDINGS.md#user-content-save-percentage) | [GAA](https://github.com/llevasseur/fantasy-hockey-league/blob/main/STANDINGS.md#user-content-goals-against-average) | Total |
| :--- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- |  -----: |
| [Kyle](https://github.com/llevasseur/fantasy-hockey-league/blob/main/ROSTERS.md#Kyle) | 6 | 7 | 6 | 5 | 8 | 5 | 8 | 8 | 53 |
| [Karter](https://github.com/llevasseur/fantasy-hockey-league/blob/main/ROSTERS.md#Karter) | 8 | 5 | 7 | 3 | 7 | 3 | 6 | 3 | 42 |
| [Alasdair](https://github.com/llevasseur/fantasy-hockey-league/blob/main/ROSTERS.md#Alasdair) | 6 | 5 | 8 | 2 | 3 | 7 | 4 | 6 | 41 |
| [Timo](https://github.com/llevasseur/fantasy-hockey-league/blob/main/ROSTERS.md#Timo) | 6 | 5 | 3 | 6 | 5 | 2 | 3 | 5 | 35 |
| [John B](https://github.com/llevasseur/fantasy-hockey-league/blob/main/ROSTERS.md#John-B) | 1 | 6 | 1 | 5 | 2 | 6 | 7 | 7 | 35 |
| [John M](https://github.com/llevasseur/fantasy-hockey-league/blob/main/ROSTERS.md#John-M) | 7 | 2 | 5 | 2 | 1 | 8 | 5 | 4 | 34 |
| [Leevon](https://github.com/llevasseur/fantasy-hockey-league/blob/main/ROSTERS.md#Leevon) | 2 | 8 | 2 | 8 | 6 | 4 | 1 | 1 | 32 |
| [Liam](https://github.com/llevasseur/fantasy-hockey-league/blob/main/ROSTERS.md#Liam) | 3 | 2 | 4 | 8 | 4 | 1 | 2 | 2 | 26 |
## Installation
Fork this repository to contribute. Commits will be analyzed before being added to the source code.
## Usage
Participants can use this github to view stats, including the Scoreboard, Selected Roosters, and Standings in each category.

To update scores:
1. Run the python script `python3 ./src/alpha-nhl/fetch-player-data.py`
2. Write manual player data to `python3 ./src/alpha-nhl/write-manual-data.py`. Input ex: FirstInitial. Lastname, SOG, M, SS, ...
3. Run `python3 ./src/alpha-nhl/merge-data.py`
4. Run `python3 ./src/alpha-nhl/data-to-md.py`
5. Run `python3 ./src/alpha-nhl/parse-standings.py`
6. Add, commit, and push changes to this github repository.
## Design Decisions: Alpha
Functional Requirements:
1. Request a response from each [eliteprospect.com](https://www.eliteprospects.com/league/wjc-20/stats/2021-2022?page=1) webpage with player statistics (page=[1,9]).
<kbd>![elite prospects webpage example](/public/images/http_source.jpg)</kbd>

Extract the html from the response and pull out data using [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/), then save data as a `json` database.

2. Some information is not provided on eliteprospect.com, including Shots on Goal and Time Played in Minutes. This information can be found on [iihf.com](https://www.iihf.com/en/events/2022/wm20/gamecenter/statistics/37416/5-lat-vs-can) or [nhl.com](https://www.nhl.com/gamecenter/bos-vs-nyr/2022/11/03/2022020161/recap/stats#game=2022020161,game_state=final,lock_state=final,game_tab=stats) game statistics summaries.
<kbd>![iihf stats summary webpage example](/public/images/additional_source.jpg)</kbd>

In the Beta version, a [selenium](https://selenium-python.readthedocs.io/) web scraper will be used, however, it has not been perfected for the alpha version. In the mean time, player data is added manually to a separate `json` file. `write-manual-data.py` is a CLI API to do this easily, taking FirstInitial. Lastname, SOG, M, SS, ... , as input. Save data as a `json` database.

3. Merge the fetched player database and the manual player database using `player_name` as the primary key. As some players have ascii characters not available on English keyboards, like `Tim Stützle`, a separate database has been created to determine player names based on the `FirstInitial. Lastname` input.

4. Display the data in 3 locations: 
* ROSTERS.md: A visualizer for each participants drafted players' statistics. 
* STANDINGS.md: A visualizer for each participants overall totals versus each other. This determines rank. 
* README.md/Scoreboard: To make the scoreboard readily available for participants when they view this github repo, the Scoreboard is attached to this README. It is a visualizer for participant points based on rank for each category (Goals, Assists, etc). Participant points determine who's winning, or who wins, and is based off the number of players.
<p align='center'><kbd><img src='/public/images/roster_example.jpg' width='450' /></kbd><kbd><img src='/public/images/standings_example.jpg' width='300' /></kbd><kbd><img src='/public/images/scoreboard_example.jpg' width='500' /></kbd></p>

## Contributing
Bug reports are welcome on Github at [Issues](https://github.com/llevasseur/world-juniors-2022/issues).
## License
This project is available as open source under the terms of the [MIT License](https://opensource.org/licenses/MIT).
## Future Work: Beta Version
Anticipated additions to this project include:
1. Automating write-manual-data.py to pull from a web scrapped website passed in. Game-specific data, including Shots on Goal (SOG) and Time Played in Minutes (TPM) can be parsed from league player data. Example, [here](https://www.nhl.com/stats/skaters).
2. Displaying data using [Matplotlib](https://matplotlib.org/).
3. Facilitate roster changes including picking up and adding players to waivers, adding players that haven't been drafted, and trades.
4. Customizable visualizers for each participant. Potentially would require a login and cloud database.