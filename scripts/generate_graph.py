from __future__ import print_function

import datetime
import sys
import numpy as np
import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt
import networkx as nx
import util

def get_query():
	query = 'select HomeTeam as home_team, AwayTeam as away_team, HomeTeamGoals as home_goals, AwayTeamGoals as away_goals, WinConditions as win_condition from WorldCupMatches'

	return query

def get_games_list(cursor):
	num_games = 0
	games = []
	for (home_team, away_team, home_goals, away_goals, win_condition) in cursor:
		winner = util.get_winner(home_goals, away_goals, win_condition)
		if winner is None:
			continue

		if winner == 'home':
			games.append((num_games, home_team, away_team, home_goals, away_goals, win_condition))
		else:
			games.append((num_games, away_team, home_team, away_goals, home_goals, win_condition))

		num_games += 1

	return games

def get_games_list_from_query(db_connection, query):
	cursor = db_connection.cursor()
	cursor.execute(query)

	games = get_games_list(cursor)

	return games

def add_header_to_games_list(games):
	games_header = [('id', 'Source', 'Target', 'Winner Goals', 'Loser Goals', 'Win Condition')]
	games = games_header + games

	return games

def strip_win_conditions(games):
	for i in range(len(games)):
		games[i] = games[i][:-1]

	return games

def generate_csv_from_query(db_connection, query):
	games = get_games_list_from_query(db_connection, query)
	games = add_header_to_games_list(games)
	games = strip_win_conditions(games)

	util.print_to_csv(games, '../world-cup-data/GamesRecord.csv')

def get_weight_of_edge(home_goals, away_goals, win_condition):
	weight = abs(home_goals - away_goals)

	return weight

def create_graph_from_games_list(games):
	graph = nx.DiGraph()

	for game in games:
		home_team = game[1]
		away_team = game[2]
		win_condition = game[5]

		winner = util.get_winner(home_team, away_team, win_condition)
		edge_weight = get_weight_of_edge(game[3], game[4], win_condition)

		if home_team not in graph:
			graph.add_node(home_team)
		if away_team not in graph:
			graph.add_node(away_team)

		graph.add_edge(home_team, away_team, weight = edge_weight)

	return graph

def generate_graph_from_query(db_connection, query):
	games = get_games_list_from_query(db_connection, query)
	graph = create_graph_from_games_list(games[1:])

	util.draw_networkx_graph(graph)

def main(argv):
	if len(argv) == 0 or not (str(argv[0]) == 'gephi' or str(argv[0]) == 'networkx'):
		print('Must include parameter: either "gephi" or "networkx"')
		return

	db_connection = util.login()
	query = get_query()

	if argv[0] == 'gephi':
		generate_csv_from_query(db_connection, query)
	else:
		generate_graph_from_query(db_connection, query)

	db_connection.close()

main(sys.argv[1:])
