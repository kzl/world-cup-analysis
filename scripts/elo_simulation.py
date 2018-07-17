from __future__ import print_function

import datetime
import math
import random
import sys
import numpy as np
import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt
import elo
import util

def get_query():
	query = 'select MatchDateTime as match_date, HomeTeam as home_team, AwayTeam as away_team, HomeTeamGoals as home_goals, AwayTeamGoals as away_goals, WinConditions as win_condition from WorldCupMatches order by MatchDateTime'

	return query

def get_elo_dict(cursor):
	elo_dict = {}

	for (match_date, home_team, away_team, home_goals, away_goals, win_condition) in cursor:
		home_won = util.get_winner(home_goals, away_goals, win_condition)
		if home_won is None:
			continue

		home_team = util.clean_country_name(home_team)
		away_team = util.clean_country_name(away_team)

		elo.update_scores(elo_dict, home_team, away_team, home_won)

	return elo_dict

def get_elo_dict_from_query(db_connection, query):
	cursor = db_connection.cursor()
	cursor.execute(query)

	elo_dict = get_elo_dict(cursor)

	return elo_dict

def print_elo_dict(elo_dict):
	sorted_elo_dict = sorted(elo_dict.items(), key = lambda x: -x[1])

	for pair in sorted_elo_dict:
		print(pair[0] + ': %.2f' % pair[1])

def main(argv):
	if len(argv) == 0:
		print('Must include paramater: either "print" or "predict"')

	db_connection = util.login()
	query = get_query()

	elo_dict = get_elo_dict_from_query(db_connection, query)

	if argv[0] == 'print':
		print_elo_dict(elo_dict)
	elif argv[0] == 'predict':
		while True:
			team_a = raw_input('Enter first team: ')
			if team_a == 'quit':
				break

			team_b = raw_input('Enter second team: ')
			if team_b == 'quit':
				break

			if util.clean_country_name(team_a) not in elo_dict:
				print('First team not recognized')
				continue
			if util.clean_country_name(team_b) not in elo_dict:
				print('Second team not recognized')
				continue

			E_a, _ = elo.get_expected_scores(elo_dict[team_a], elo_dict[team_b])

			print('Chance that ' + util.clean_country_name(team_a) + ' will win: %.2f' % (100.0 * E_a) + '%\n')

main(sys.argv[1:])
