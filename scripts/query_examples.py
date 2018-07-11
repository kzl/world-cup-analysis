from __future__ import print_function

import datetime
import mysql.connector

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

cnx = mysql.connector.connect(user = 'user', password = 'pass123!', host = '127.0.0.1', database = 'world_cup')
cursor = cnx.cursor()

query = 'select MatchDateTime as match_date, HomeTeam as home_team, AwayTeam as away_team, HomeTeamGoals as home_goals, AwayTeamGoals as away_goals from WorldCupMatches where HomeTeam = "Germany" or AwayTeam = "Germany";'

cursor.execute(query)

record = []
dates = []
for (match_date, home_team, away_team, home_goals, away_goals) in cursor:
	if ((home_team == 'Germany' and home_goals > away_goals) or (away_team == 'Germany' and home_goals < away_goals)):
		record.append(1)
	elif ((home_team == 'Germany' and home_goals < away_goals) or (away_team == 'Germany' and home_goals > away_goals)):
		record.append(-1)
	else:
		record.append(0)
	print(match_date)
	dates.append(match_date)#.strftime('%Y-%m-%d'))

series = pd.Series(record, index = dates)
series = series.cumsum()

plt.figure()
series.plot()
plt.show()

cursor.close()
cnx.close()
