from __future__ import print_function

import datetime
import sys
import numpy as np
import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt

def get_countries(argv):
	countries = []
	if len(sys.argv) > 0:
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

	return username[:-1], password[:-1], ip_address[:-1]

def login(database = 'world_cup'):
	username, password, ip_address = get_credentials()
	db_connection = mysql.connector.connect(user = username, password = password, host = ip_address, database = database)

	return db_connection

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
