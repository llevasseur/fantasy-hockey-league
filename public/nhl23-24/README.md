# Fantasy Hockey League
### Beta Version: Data parsed with Selenium from nhl.com
Casual Python3 project used by friends to keep track of NHL players stats. Statistics of players drafted by participants are totaled to determine Scoreboard ranking and to determine the winner.

Find me on Mastodon! <a rel="me" href="https://techhub.social/@leevonlevasseur">Mastodon</a>
## Scoreboard
[TODO]
## Installation
Fork this repository to contribute. Commits will be analyzed before being added to the source code.
## Usage
Participants can use this github to view stats, including the Scoreboard, Selected Roosters, and Standings in each category.

[TODO]
## Design Decisions: Beta
Functional Requirements:
1. Request the [Selenium](https://selenium-python.readthedocs.io/) Chrome driver to extract all player data from each [hockeystatcards.com/all-skaters](https://www.hockeystatcards.com/all-skaters) webpage with player statistics (page=[0,27]) and pageSize=50.
<kbd>![nhl.com stats webpage example](/public/images/hockeyStatCards.jpg)</kbd>

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