from __future__ import print_function
from __future__ import division

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

def get_confidence_bracket(win_percent):
	brackets = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

	confidence_percent = max(win_percent, 1.0 - win_percent)

	index = 0
	while confidence_percent > brackets[index]:
		index += 1

	return index

def get_elo_dict(cursor, analyze):
	elo_dict = {}

	correct_results = [0, 0, 0, 0, 0, 0]
	incorrect_results = [0, 0, 0, 0, 0, 0]

	for (match_date, home_team, away_team, home_goals, away_goals, win_condition) in cursor:
		home_won = util.get_winner(home_goals, away_goals, win_condition)
		if home_won is None:
			continue

		home_team = util.clean_country_name(home_team)
		away_team = util.clean_country_name(away_team)

		if home_team in elo_dict and away_team in elo_dict and analyze:
			E_a, E_b = elo.get_expected_scores(elo_dict[home_team], elo_dict[away_team])
			bracket_index = get_confidence_bracket(E_a)

			if E_a > E_b:
				if home_won:
					correct_results[bracket_index] += 1
				else:
					incorrect_results[bracket_index] += 1

			elif E_a < E_b:
				if home_won:
					incorrect_results[bracket_index] += 1
				else:
					correct_results[bracket_index] += 1

		elo.update_scores(elo_dict, home_team, away_team, home_won)

	if not analyze:
		return elo_dict
	else:
		results = [0, 0, 0, 0, 0, 0]
		for i in range(6):
			if i == 0:
				continue

			if correct_results[i] + incorrect_results[i] == 0:
				results[i] = None
			else:
				results[i] = correct_results[i] / (correct_results[i] + incorrect_results[i])

		return results

def get_elo_dict_from_query(db_connection, query, analyze = False):
	cursor = db_connection.cursor()
	cursor.execute(query)

	result = get_elo_dict(cursor, analyze)

	return result

def print_elo_dict(elo_dict):
	sorted_elo_dict = sorted(elo_dict.items(), key = lambda x: -x[1])

	for pair in sorted_elo_dict:
		print(pair[0] + ': %.2f' % pair[1])

def main(argv):
	if len(argv) == 0:
		print('Must include paramater: either "print", "predict", or "analyze"')

	db_connection = util.login()
	query = get_query()

	if argv[0] == 'print':
		elo_dict = get_elo_dict_from_query(db_connection, query)

		print_elo_dict(elo_dict)

	elif argv[0] == 'predict':
		elo_dict = get_elo_dict_from_query(db_connection, query)

		while True:
			team_a = raw_input('Enter first team: ')
			if team_a == 'quit':
				break
			if util.clean_country_name(team_a) not in elo_dict:
				print('Team not recognized')
				continue

			team_b = raw_input('Enter second team: ')
			if team_b == 'quit':
				break
			if util.clean_country_name(team_b) not in elo_dict:
				print('Team not recognized')
				continue

			E_a, _ = elo.get_expected_scores(elo_dict[team_a], elo_dict[team_b])

			print('Chance that ' + util.clean_country_name(team_a) + ' will win: %.2f' % (100.0 * E_a) + '%\n')

	elif argv[0] == 'analyze':
		results = get_elo_dict_from_query(db_connection, query, analyze = True)

		brackets = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
		for i in range(6):
			if i == 0:
				continue

			if results[i] is None:
				print(str(brackets[i-1]) + ' - ' + str(brackets[i]) + ': no data')
			else:
				print(str(brackets[i-1]) + ' - ' + str(brackets[i]) + ': ' + '%.2f' % (100.0 * results[i]))

main(sys.argv[1:])
