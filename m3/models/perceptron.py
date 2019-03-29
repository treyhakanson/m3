from sklearn.linear_model import Perceptron
import numpy as np
import json 
import warnings

import data_wrangling

warnings.filterwarnings("ignore")

class MMPerceptron:
	def __init__(self):
		with open('../cleaned-data/binary-data.json', 'r') as f:
			self.training_data = json.loads(f.read())
		self.models = { team: Perceptron(random_state=0, max_iter=10) for team in self.training_data.keys()}
		self.feature_vectors = data_wrangling.import_feature_vectors()

	def train(self):
		for team, model in self.models.items():
			model.fit(np.array(self.training_data[team]['X']), np.array(self.training_data[team]['Y']))

	def predict(self, team, opponent):
		return self.models[team].predict(np.array([self.feature_vectors[team] + self.feature_vectors[opponent]]))[0]
