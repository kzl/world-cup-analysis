from __future__ import print_function
from enum import Enum

import datetime
import sys
import numpy as np
import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt
import networkx as nx

class Stage(Enum):
	__order__ = 'GROUPS Ro16 QUARTERS SEMIS FINALS'
	GROUPS = 1
	Ro16 = 2
	QUARTERS = 3
	SEMIS = 4
	FINALS = 5

def get_countries(argv):
	countries = []
	if len(argv) > 0:
		for arg in argv:
			countries.append(arg)
	else:
		print('No argument entered. You must enter the name of at least one country to query.')

	return countries

def get_credentials():
	file = open('../setup/credentials.txt', 'r')
	username = file.readline()
	password = file.readline()
	ip_address = file.readline()
	file.close()

	return username[:-1], password[:-1], ip_address[:-1]

def login(database = 'world_cup'):
	username, password, ip_address = get_credentials()
	db_connection = mysql.connector.connect(user = username, password = password, host = ip_address, database = database)

	return db_connection

def get_winner(home_goals, away_goals, win_condition):
	winner = None

	if home_goals > away_goals:
		winner = 'home'
	elif home_goals < away_goals:
		winner = 'away'
	else:
		if win_condition != '':
			for i in range(len(win_condition)):
				if win_condition[i] == '(':
					if int(win_condition[i+1]) > int(win_condition[i+5]):
						winner = 'home'
					else:
						winner = 'away'
					break

	return winner

def get_stage(stage_name):
	stage = None
	stage_name = stage_name.lower()

	if stage_name[0] == 'g':
		stage = Stage.GROUPS
	elif stage_name[0] == 'r':
		stage = Stage.Ro16
	elif stage_name[0] == 'q':
		stage = Stage.QUARTERS
	elif stage_name[0] == 's':
		stage = Stage.SEMIS
	elif stage_name == 'final':
		stage = Stage.FINALS

	return stage

def plot_time_series(series):
	if series.size > 0:
		plt.figure()
		series.plot()
		plt.show()
	else:
		print('No data found to plot.')

def plot_histogram(series, alpha = 0.5):
	if series.size > 0:
		plt.figure()
		series.plot.hist(alpha = alpha)
		plt.show()
	else:
		print('No data found to plot.')

def plot_bar_graph(series):
	if series.size > 0:
		plt.figure()
		series.plot.bar()
		plt.show()
	else:
		print('No data found to plot')

def draw_networkx_graph(graph):
	nx.draw_spring(graph, with_labels = True, alpha = 0.7, font_size = 6)
	plt.show()

def print_to_csv(data, file_name):
	file = open(file_name, 'w')

	for row in data:
		for i in range(len(row)):
			if type(row[i]) is int:
				file.write(str(row[i]))
			else:
				file.write(row[i].encode('utf-8'))
			if i == len(row)-1:
				file.write('\n')
			else:
				file.write(',')

	file.close()
