from __future__ import print_function

import datetime
import sys
import numpy as np
import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt
import util

def get_queries(countries):
	queries = []
	for country in countries:
		if country == 'Germany' or country == 'Germany FR':
			queries.append((country, 'select HomeTeam as home_team, AwayTeam as away_team, HomeTeamGoals as home_goals, AwayTeamGoals as away_goals from WorldCupMatches where HomeTeam = "Germany" or AwayTeam = "Germany" or HomeTeam = "Germany FR" or AwayTeam = "Germany FR";'))
		else:
			queries.append((country, 'select HomeTeam as home_team, AwayTeam as away_team, HomeTeamGoals as home_goals, AwayTeamGoals as away_goals from WorldCupMatches where HomeTeam = "' + country + '" or AwayTeam = "' + country + '";'))
	
	return queries

def get_country_series(cursor, country, max_goals_range = 10):
	if cursor is None:
		print('No data found.')
		return

	num_goals = {}
	for goals in range(max_goals_range+1):
		num_goals[goals] = 0

	total_goals = 0
	num_games = 0

	for (home_team, away_team, home_goals, away_goals) in cursor:
		num_games += 1

		if (home_team == country):
			num_goals[home_goals] += 1
			total_goals += home_goals
		else:
			num_goals[away_goals] += 1
			total_goals += away_goals

		if country == 'Germany':
			if (home_team == 'Germany FR'):
				num_goals[home_goals] += 1
				total_goals += home_goals
			else:
				num_goals[away_goals] += 1
				total_goals += away_goals

	average_goals = float(total_goals) / float(num_games)

	goals_freq = []
	for goals in range(max_goals_range):
		goals_freq.append(num_goals[goals])

	series = pd.Series(goals_freq)
	series.name = country

	print('%(country)s has scored %(total)d total goals and averages %(average).2f goals per match' % {'country': country, 'total': total_goals, 'average': average_goals})

	return series

def get_series_from_queries(db_connection, queries):
	cursor = db_connection.cursor()
	series_list = []
	for country, query in queries:
		cursor.execute(query)
		series = get_country_series(cursor, country)
		series_list.append(series)

	cursor.close()

	series_data = pd.concat(series_list, axis = 1)

	return series_data

def main(argv):
	countries = util.get_countries(argv)
	if len(countries) == 0:
		return

	db_connection = util.login()
	queries = get_queries(countries)
	series = get_series_from_queries(db_connection, queries)

	util.plot_bar_graph(series)

	db_connection.close()

main(sys.argv[1:])
