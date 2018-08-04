# world-cup-analysis

Analysis of world cup data, including records, goals, and audience attraction

## Results

### Top Statistics

The team with the best record (wins - losses) is Brazil, at 55.

The team with the most goals scored overall is Germany, with 350 total goals.

The team with the highest average goals scored is Germany, with 3.30 goals per match.

### Elo Ratings

| Rank | Country | Elo Rating |
| :---: | :--- | :---: |
| 1 | Brazil | 1825.37 |
| 2 | Germany | 1772.87 |
| 3 | Argentina | 1763.83 |
| 4 | Italy | 1847.03 |
| 5 | Netherlands | 1699.77 |
| 6 | Sweden | 1687.21 |
| ... | ... | ... |
| 8 | England | 1669.83 |
| 12 | Australia | 1640.54 |
| 16 | France | 1630.51 |
| 29 | USA | 1610.60 |
| 35 | Japan | 1598.43 |
| 51 | Canada | 1583.95 |
| ... | ... | ... |
| 76 | Republic of Ireland | 1528.57 |
| 77 | Iran | 1527.75 |
| 78 | El Salvador | 1510.16 |
| 79 | Croatia | 1507.50 |
| 80 | Bulgaria | 1506.49 |
| 81 | Mexico | 1500.92 |

Prior to the events of the 2018 World Cup, the model predicted that in a game between France and Croatia, France had a 67.00% chance to win.

### Accuracy of Elo Predictions

| % Interval | Accuracy |
| :---: | :---: |
| 50% - 60% | 51.26% |
| 60% - 70% | 63.64% |
| 70% - 80% | 73.47% |
| 80% - 90% | 75.00% |
| 90% - 100% | n/a |

ex. In all games where one team had a chance to win between 50% and 60%, the model was correct 51.26% of the time.

### Included Graphs

In the Audience Graphs folder, graphs display by stage the audience size of each game over time.

The World Cup Game Records graph shows the win/loss relationships between countries – the center node is Brazil.

The World Cup Goals graph shows the distribution of the frequencies of the number of goals scored in a game for selected countries.

The World Cup Records graph shows the record (wins - losses) of selected teams over time.

## Setup

### Dataset

The data used for this analysis came from Andre Becklas on Kaggle: [link to dataset](https://www.kaggle.com/abecklas/fifa-world-cup).

Note: since the dataset was created before the 2018 World Cup, the results presented do not include the 2018 results.

### Tools Used

Python 2, C++, MySQL
