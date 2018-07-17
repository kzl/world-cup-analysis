from __future__ import print_function

import math

def get_K_factor(rating):
	K_dict = { 2400: 12, 2000: 24, 0: 32}

	K = 12
	for rating_tier in K_dict:
		if rating >= rating_tier:
			K = K_dict[rating_tier]
			break

	return K

def get_default_rating():
	default_rating = 1600

	return default_rating

def get_expected_scores(rating_a, rating_b):
	Q_a = 10.0**(rating_a/400.0)
	Q_b = 10.0**(rating_b/400.0)

	E_a = Q_a / (Q_a + Q_b)
	E_b = Q_b / (Q_a + Q_b)

	return E_a, E_b

def update_scores(rating_dict, player_a, player_b, a_won):
	if player_a not in rating_dict:
		rating_dict[player_a] = get_default_rating()
	if player_b not in rating_dict:
		rating_dict[player_b] = get_default_rating()

	E_a, E_b = get_expected_scores(rating_dict[player_a], rating_dict[player_b])
	S_a = 1 if a_won else 0

	rating_dict[player_a] += get_K_factor(rating_dict[player_a]) * (S_a - E_a)
	rating_dict[player_b] += get_K_factor(rating_dict[player_b]) * (1.0 - S_a - E_b)
