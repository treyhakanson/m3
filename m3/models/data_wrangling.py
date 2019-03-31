import pandas as pd
import numpy as np 
import os
import json
import re 

pd.set_option('display.expand_frame_repr', False)

TRAINING_DIR = './schedules'
FEATURE_DIR = './feature-vectors'
MATCHUPS_DIR = './matchups'

def gentle_clean_opponent_name(name):
  name = re.sub(r'\s*\(\d+\)', '', name)       # Remove ranking
  name = re.sub(r'[^a-zA-Z0-9_ -]', '', name)  # Remove special characters
  name = re.sub(r'[\s-]+', '-', name)          # Spaces -> hyphens
  name = name.lower()                          # Lowercase string
  return name

OPPONENT_MAP = {
  "purdue-fort-wayne": "ipfw",
  "little-rock": "arkansas-little-rock",
  "omaha": "nebraska-omaha",
  "st-johns": "st-johns-ny",
  "st-marys": "saint-marys-ca",
  "university-of-california": "california",
  "uc-irvine": "california-irvine",
  "uc-merced": "california-merced",
  "uc-davis": "california-davis",
  "uc-santa-cruz": "california-santa-cruz",
  "uc-riverside": "california-riverside",
  "uc-santa-barbara": "california-santa-barbara",
  "southeastern": "southeastern-louisiana",
  "louisiana": "louisiana-lafayette",
  "texas-rio-grande-valley": "texas-pan-american",
  "point-university": "point",
  "bethesda-university-ca": "bethesda-ca",
  "penn-st-brandywine": "penn-state-brandywine",
  "bob-jones-university": "bob-jones",
  "southeastern-oklahoma-state": "southeastern-oklahoma",
  "southeastern-baptist-college": "se-baptist",
  "missouri-baptist-university": "missouri-baptist",
  "penn-st-wilkes-barre": "penn-state-wilkes-barre",
  "florida-national-university": "florida-national"
}

def _import_training_data(feature_teams):
	training_data = {}
	for fname in os.listdir(TRAINING_DIR):
		if fname.endswith(".csv"):
			schedule = pd.read_csv(os.path.join(TRAINING_DIR, fname), index_col=0)
			schedule['Opponent'] = schedule['Opponent'].apply(lambda n: gentle_clean_opponent_name(n))
			schedule['Opponent'] = schedule['Opponent'].apply(lambda n: OPPONENT_MAP.get(n, n))
			training_data[fname.replace('-schedule.csv', '')] = schedule

	cleaned_training_data = {team: [] for team in training_data.keys()}
	for team, data in training_data.items():
		for index, row in data.iterrows():
			if row['Opponent'] in feature_teams and not np.isnan(row['Team Points']) and not np.isnan(row['Opponent Points']):
				cleaned_training_data[team].append({
					'opponent': row['Opponent'],
					'outcome': 1 if row['Outcome'] == 'W' else 0,
					'ratio': row['Team Points']/row['Opponent Points']
				})
	return cleaned_training_data

def _import_feature_vectors():
	feature_vectors = {}
	for fname in os.listdir(FEATURE_DIR):
		if fname.endswith(".csv"):
			team = fname.replace('.csv', '')
			feature_vectors[team] = pd.read_csv(os.path.join(FEATURE_DIR, fname), index_col=0).values.flatten().tolist()
	return feature_vectors

def _import_training_teams():
	teams = []
	for fname in os.listdir(MATCHUPS_DIR):
		if fname.endswith(".csv"):
			matchups = pd.read_csv(os.path.join(MATCHUPS_DIR, fname))
			for index, row in matchups.iterrows():
				teams.append(row['School 1 Name'])
				teams.append(row['School 2 Name'])
	return teams

def gimme_data():
	feature_vectors = _import_feature_vectors()
	training_data = _import_training_data(feature_vectors.keys())
	qualified_teams = _import_training_teams()

	pre_processed_data = {team: { 'X': [], 'Y': [] } for team in qualified_teams}
	for team in qualified_teams:
		for game in training_data[team]:
			pre_processed_data[team]['X'].append(feature_vectors[team] + feature_vectors[game['opponent']])
			pre_processed_data[team]['Y'].append(game['ratio'])
	return pre_processed_data

def dump():
	data = gimme_data()
	with open('./cleaned-data/point-ratio-data.json', 'w') as f:
		json.dump(data, f)

dump()