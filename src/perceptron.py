from sklearn.linear_model import Perceptron
import pandas as pd 
import os

import utils
import constants 

pd.set_option('display.expand_frame_repr', False)

TRAINING_DIR = '../schedules'
FEATURE_DIR = '../feature-vectors'

def import_training_data():
	results = {}
	for fname in os.listdir(TRAINING_DIR):
		if fname.endswith(".csv"): 
			schedule = pd.read_csv(os.path.join(TRAINING_DIR, fname))
			schedule['Opponent'] = schedule['Opponent'].apply(lambda n: utils.gentle_clean_opponent_name(n))
			schedule['Opponent'] = schedule['Opponent'].apply(lambda n: constants.OPPONENT_MAP.get(n, n))
			results[fname.replace('-schedule.csv', '')] = schedule
	return results

def import_feature_vectors():
	results = {}
	for fname in os.listdir(FEATURE_DIR):
		if fname.endswith(".csv"): 
			results[fname.replace('csv', '')] = pd.read_csv(os.path.join(FEATURE_DIR, fname))
	return results

def main():
	perceptron = Perceptron(random_state=0)
	training_data = import_training_data()
	feature_vectors = import_feature_vectors()
	# print(training_data['arizona-state'].head())
	feature_teams = set(feature_vectors.keys())
	training_teams = set()
	for train in training_data.values():
		training_teams.update(train['Opponent'])

	print(training_teams.difference(feature_teams))

main()
