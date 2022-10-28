# Hockey League Fantasy Draft
Casual Python3 project used by friends to keep track of NHL and WJC players' stats. Statistics of players drafted by participants are totaled to determine Scoreboard ranking and to determine the winner.
## Scoreboard
| User | [G](https://github.com/llevasseur/world-juniors-2022/blob/master/STANDINGS.md#goals) | [A](https://github.com/llevasseur/world-juniors-2022/blob/master/STANDINGS.md#assists) | [SOG](https://github.com/llevasseur/world-juniors-2022/blob/master/STANDINGS.md#shots-on-goal) | [PIM](https://github.com/llevasseur/world-juniors-2022/blob/master/STANDINGS.md#penalties-in-minutes) | [+/-](https://github.com/llevasseur/world-juniors-2022/blob/master/STANDINGS.md#plus--minus) | [TPM](https://github.com/llevasseur/world-juniors-2022/blob/master/STANDINGS.md#time-played-in-minutes) | [S%](https://github.com/llevasseur/world-juniors-2022/blob/master/STANDINGS.md#save-percentage) | [GAA](https://github.com/llevasseur/world-juniors-2022/blob/master/STANDINGS.md#goals-against-average) | Total |
| :--- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- |  -----: |
| [Timo](https://github.com/llevasseur/world-juniors-2022/blob/master/ROSTERS.md#Timo) | 5 | 6 | 6 | 2 | 5 | 6 | 1 | 1 | 32 |
| [Liam](https://github.com/llevasseur/world-juniors-2022/blob/master/ROSTERS.md#Liam) | 3 | 2 | 5 | 6 | 2 | 1 | 6 | 6 | 31 |
| [Alasdair](https://github.com/llevasseur/world-juniors-2022/blob/master/ROSTERS.md#Alasdair) | 6 | 5 | 4 | 3 | 6 | 2 | 2 | 2 | 30 |
| [Leevon](https://github.com/llevasseur/world-juniors-2022/blob/master/ROSTERS.md#Leevon) | 2 | 4 | 1 | 5 | 3 | 5 | 3 | 6 | 29 |
| [John](https://github.com/llevasseur/world-juniors-2022/blob/master/ROSTERS.md#John) | 1 | 4 | 2 | 5 | 4 | 4 | 5 | 4 | 29 |
| [Carsten](https://github.com/llevasseur/world-juniors-2022/blob/master/ROSTERS.md#Carsten) | 4 | 2 | 3 | 1 | 1 | 3 | 4 | 3 | 21 |
## Installation
Fork this repository to contribute. Commits will be analyzed before being added to the source code.
## Usage
Participants can use this github to view stats, including the Scoreboard, Selected Roosters, and Standings in each category.

To update scores:
1. Run the python script `python ./src/fetch-player-data.py`
2. Write manual player data to `python ./src/write-manual-data.py`. Input ex: Firstname1 Lastname1,SOG,MM,SS, ...
3. Run `python ./src/merge-data.py`
4. Run `python ./src/data-to-md.py`
5. Run `python ./src/parse-standings.py`
6. Add, commit, and push changes to this github repository.
## Design Decisions
Functional Requirements:
1. Request a response from each [eliteprospect.com](https://www.eliteprospects.com/league/wjc-20/stats/2021-2022?page=1) webpage with player statistics (page=[1,4]).
<kbd>![elite prospects webpage example](/public/images/http_source.jpg)</kbd>

Extract the html from the response and pull out data using [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/), then save data as a `json` database.

2. Some information is not provided on eliteprospect.com, including Shots on Goal and Time Played in Minutes. This information can be found on [iihf.com](https://www.iihf.com/en/events/2022/wm20/gamecenter/statistics/37416/5-lat-vs-can) game statistics summaries.
<kbd>![iihf stats summary webpage example](/public/images/additional_source.jpg)</kbd>

A web scraper has not been constructed for this website yet so player data is added manually to a separate `json` file. `write-manual-data.py` is a CLI API to do this easily, taking Firstname1 Lastname1,SOG,MM,SS, ... , as input. Save data as a `json` database.

3. Merge the fetched player database and the manual player database using `player_name` as the primary key.

4. Display the data in 3 locations: 
* ROSTERS.md: A visualizer for each participants drafted players' statistics. 
* STANDINGS.md: A visualizer for each participants overall totals versus each other. This determines rank. 
* README.md/Scoreboard: To make the scoreboard readily available for participants when they view this github repo, the Scoreboard is attached to this README. It is a visualizer for participant points based on rank for each category (Goals, Assists, etc). Participant points determine who's winning, or who wins, and is based off the number of players.
<p align='center'><kbd><img src='/public/images/roster_example.jpg' width='450' /></kbd><kbd><img src='/public/images/standings_example.jpg' width='300' /></kbd><kbd><img src='/public/images/scoreboard_example.jpg' width='500' /></kbd></p>

## Contributing
Bug reports are welcome on Github at [Issues](https://github.com/llevasseur/world-juniors-2022/issues).
## License
This project is available as open source under the terms of the [MIT License](https://opensource.org/licenses/MIT).
## Future Work
Anticipated additions to this project include:
1. Automating write-manual-data.py to pull from a web scrapped website passed in. Game-specific data, including Shots on Goal (SOG) and Time Played in Minutes (TPM) can be parsed from player data. Example, [here](https://www.iihf.com/en/events/2022/wm20/gamecenter/statistics/37416/5-lat-vs-can).
2. Displaying data using [Matplotlib](https://matplotlib.org/).
3. Increasing scale of project to work for more leagues, like the [NHL](https://www.eliteprospects.com/league/nhl).
4. Handling automated input for names with unfamiliar unicode, like `Topi Niemelä`.