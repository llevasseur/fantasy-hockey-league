# World Junior Fantasy Draft
Casual Python3 project used by friends to keep track of World Junior hockey players' stats. Statistics of players drafted by participants are totaled to determine Scoreboard ranking and to determine the winner.
## Scoreboard
| User | [G](https://github.com/llevasseur/world-juniors-2022/blob/master/STANDINGS.md#goals) | [A](https://github.com/llevasseur/world-juniors-2022/blob/master/STANDINGS.md#assists) | SOG | [PIM](https://github.com/llevasseur/world-juniors-2022/blob/master/STANDINGS.md#penalties-in-minutes) | [+/-](https://github.com/llevasseur/world-juniors-2022/blob/master/STANDINGS.md#plus--minus) | TPM | [S%](https://github.com/llevasseur/world-juniors-2022/blob/master/STANDINGS.md#save-percentage) | [GAA](https://github.com/llevasseur/world-juniors-2022/blob/master/STANDINGS.md#goals-against-average) | Total |
| :--- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- |  -----: |
| [John](https://github.com/llevasseur/world-juniors-2022/blob/master/ROSTERS.md#John) | 5 | 4 | 5 | 2 | 5 | 2 | 2 | 2 | 27 |
| [Alasdair](https://github.com/llevasseur/world-juniors-2022/blob/master/ROSTERS.md#Alasdair) | 4 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 25 |
| [Leevon](https://github.com/llevasseur/world-juniors-2022/blob/master/ROSTERS.md#Leevon) | 3 | 5 | 4 | 1 | 5 | 5 | 1 | 1 | 25 |
| [Liam](https://github.com/llevasseur/world-juniors-2022/blob/master/ROSTERS.md#Liam) | 2 | 2 | 2 | 4 | 2 | 4 | 4 | 4 | 24 |
| [Timo](https://github.com/llevasseur/world-juniors-2022/blob/master/ROSTERS.md#Timo) | 1 | 1 | 1 | 5 | 1 | 1 | 5 | 5 | 20 |
## Installation
Request to fork this repository to contribute. Commits will be analyzed before being added to the source code.
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
[Todo]
## Contributing
Bug reports are welcome on Github at [Issues](https://github.com/llevasseur/world-juniors-2022/issues).
## License
This gem is available as open source under the terms of the [MIT License](https://opensource.org/licenses/MIT).
## Future Work
Anticipated additions to this project include:
1. Automating write-manual-data.py to pull from a web scrapped website passed in. Game-specific data, including Shots on Goal (SOG) and Total Minutes Played (TMP) can be parsed from player data. Example, [here](https://www.iihf.com/en/events/2022/wm20/gamecenter/statistics/37416/5-lat-vs-can).
2. Display data using [Matplotlib](https://matplotlib.org/).
3. Increase scale of project to work for multiple leagues, like [NHL](https://www.eliteprospects.com/league/nhl).