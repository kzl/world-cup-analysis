from __future__ import print_function
from sklearn import linear_model, metrics, neighbors

import datetime
import math
import random
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

def get_valid_models():
	models_list = ['linear', 'knn']

	return models_list

def split_xy_data(data):
	x = np.zeros((len(data), 1), dtype = np.float64)
	y = np.zeros((len(data), 1), dtype = np.float64)

	for i in range(len(data)):
		x[i][0] = data[i][0]
		y[i][0] = data[i][1]

	return x, y

def split_data(data, train_pct = 0.8):
	num_training_examples = int(math.floor(train_pct * len(data)))

	random.shuffle(data)

	training_data = data[:num_training_examples]
	test_data = data[num_training_examples:]

	train_x, train_y = split_xy_data(training_data)
	test_x, test_y = split_xy_data(test_data)

	return train_x, train_y, test_x, test_y

def print_model_variables(regr):
	print('Slope:\n', regr.coef_)
	print('y-Intercept:\n', regr.intercept_)

def print_model_results(test_y, test_predictions):
	print('Mean Squared Error: %.2f' % metrics.mean_squared_error(test_y, test_predictions))
	print('Variance: %.2f' % metrics.r2_score(test_y, test_predictions))

def graph_model_results(train_x, train_y, test_x, test_y, test_predictions, color = 'black'):
	plt.scatter(train_x, train_y, color = color)
	plt.scatter(test_x, test_y, color = color)
	plt.plot(test_x, test_predictions, color = 'crimson')

	plt.show()

def generate_model(data, model = 'linear', show_results = True, color = 'black'):
	train_x, train_y, test_x, test_y = split_data(data)

	regr = None
	if model == 'linear':
		regr = linear_model.LinearRegression()
	elif model == 'knn':
		regr = neighbors.KNeighborsRegressor(8)

	regr.fit(train_x, train_y)

	test_predictions = regr.predict(test_x)

	if show_results:
		if model == 'linear':
			print_model_variables(regr)
		
		print_model_results(test_y, test_predictions)
		graph_model_results(train_x, train_y, test_x, test_y, test_predictions, color)

	return regr

def main(argv):
	if len(argv) == 0 or not (str(argv[0]) == 'graph' or str(argv[0]) == 'build_model'):
		print('Must include parameter: either "graph" or "build_model"')
		return

	db_connection = util.login()
	query = get_query()

	if argv[0] == 'graph':
		attendance_table = get_attendance_table_from_query(db_connection, query)
		stages_data = convert_table_to_series(attendance_table)
		plot_stages_data(stages_data)

	elif argv[0] == 'build_model':
		if len(argv) == 1:
			print('Must include parameter for build_model')
			return

		models_list = get_valid_models()
		model = argv[1]

		if model in models_list:
			attendance_table = get_attendance_table_from_query(db_connection, query)
			stages_data = convert_table_to_series(attendance_table)

			for stage in util.Stage:
				print(stage)
				generate_model(stages_data[stage], model = model, show_results = True, color = get_stage_color(stage))
		else:
			print('Invalid model name')

	db_connection.close()

main(sys.argv[1:])
