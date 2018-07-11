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
			queries.append((country, 'select ChampionshipYear as year, HomeTeam as home_team, AwayTeam as away_team, HomeTeamGoals as home_goals, AwayTeamGoals as away_goals from WorldCupMatches where HomeTeam = "Germany" or AwayTeam = "Germany" or HomeTeam = "Germany FR" or AwayTeam = "Germany FR";'))
		else:
			queries.append((country, 'select ChampionshipYear as year, HomeTeam as home_team, AwayTeam as away_team, HomeTeamGoals as home_goals, AwayTeamGoals as away_goals from WorldCupMatches where HomeTeam = "' + country + '" or AwayTeam = "' + country + '";'))
	
	return queries

def get_country_series(cursor, country, range_min, range_max):
	yearly_records= {}
	for year in range(range_min, range_max+1):
		yearly_records[year] = 0

	for (year, home_team, away_team, home_goals, away_goals) in cursor:
		if ((home_team == country and home_goals > away_goals) or (away_team == country and home_goals < away_goals)):
			yearly_records[year] = yearly_records.get(year) + 1;
		elif ((home_team == country and home_goals < away_goals) or (away_team == country and home_goals > away_goals)):
			yearly_records[year] = yearly_records.get(year) - 1;

		if country == 'Germany':
			if ((home_team == 'Germany FR' and home_goals > away_goals) or (away_team == 'Germany FR' and home_goals < away_goals)):
				yearly_records[year] = yearly_records.get(year) + 1;
			elif ((home_team == 'Germany FR' and home_goals < away_goals) or (away_team == 'Germany FR' and home_goals > away_goals)):
				yearly_records[year] = yearly_records.get(year) - 1;

	full_record = []
	current_record = 0
	for year in range(range_min, range_max+1):
		for i in range(365):
			full_record.append(current_record)
		if year % 4 == 0:
			full_record.append(current_record)
		current_record += yearly_records.get(year)

	num_periods = len(full_record)
	series = pd.Series(full_record, pd.date_range('1/1/' + str(range_min), periods = num_periods))
	series.name = country

	return series

def get_series_from_queries(db_connection, queries, range_min = 1930, range_max = 2015):
	cursor = db_connection.cursor()
	series_list = []
	for country, query in queries:
		cursor.execute(query)
		series = get_country_series(cursor, country, range_min, range_max)
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
	series = get_series_from_queries(db_connection, queries, 1930, 2018)

	util.plot_time_series(series)

	db_connection.close()

main(sys.argv[1:])
