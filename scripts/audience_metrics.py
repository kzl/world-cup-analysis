from __future__ import print_function

import datetime
import sys
import numpy as np
import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt
import util

def get_query():
	query = 'select ChampionshipYear as year, HomeTeam as home_team, AwayTeam as away_team, Stage as stage_name, Attendance as audience_size from WorldCupMatches'

	return query

def get_attendance_table(cursor):
	attendance_table = []

	for (year, home_team, away_team, stage_name, audience_size) in cursor:
		stage = util.get_stage(stage_name)
		if stage is None:
			continue

		attendance_table.append((year, home_team, away_team, stage, audience_size))

	return attendance_table

def get_attendance_table_from_query(db_connection, query):
	cursor = db_connection.cursor()
	cursor.execute(query)

	attendance_table = get_attendance_table(cursor)

	return attendance_table

def convert_table_to_series(attendance_table):
	stages_data = {}

	for stage in util.Stage:
		stages_data[stage] = []

	for game in attendance_table:
		stages_data[game[3]].append((game[0], game[4]))

	return stages_data

def get_stage_color(stage):
	color = None

	if stage == util.Stage.GROUPS:
		color = 'darkblue'
	elif stage == util.Stage.Ro16:
		color = 'lightgreen'
	elif stage == util.Stage.QUARTERS:
		color = 'orange'
	elif stage == util.Stage.SEMIS:
		color = 'violet'
	elif stage == util.Stage.FINALS:
		color = 'crimson'

	return color

def plot_stages_data(stages_data):
	plt.figure()
	for stage in util.Stage:
		dataframe = pd.DataFrame(data = stages_data[stage], columns = ['year', 'audience'])
		dataframe.plot(kind = 'scatter', x = 'year', y = 'audience', color = get_stage_color(stage))

	plt.show()

def main(argv):
	if len(argv) == 0 or not (str(argv[0]) == 'graph' or str(argv[1]) == 'build_model'):
		print('Must include parameter: either "graph" or "build_model"')
		return

	db_connection = util.login()
	query = get_query()

	if argv[0] == 'graph':
		attendance_table = get_attendance_table_from_query(db_connection, query)
		stages_data = convert_table_to_series(attendance_table)
		plot_stages_data(stages_data)

	else:
		pass

	db_connection.close()

main(sys.argv[1:])
