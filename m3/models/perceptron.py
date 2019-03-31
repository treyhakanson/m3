from sklearn.linear_model import Perceptron
from sklearn.neural_network import MLPClassifier
import numpy as np
import warnings

from matchup_model import MatchupModel

warnings.filterwarnings("ignore")

class MMPerceptron(MatchupModel):
	def __init__(self):
		super().__init__()
		self.models = { team: Perceptron(random_state=0, max_iter=10) for team in self.training_data.keys()}
		self.model_name = "perceptron"

	def train(self):
		for team, model in self.models.items():
			model.fit(np.array(self.training_data[team]['X']), np.array(self.training_data[team]['Y']))

	def predict(self, team, opponent):
		return self.models[team].predict(np.array([self.create_matchup_feature_vector(team, opponent)]))[0]

class MMMultilayerPerceptron(MatchupModel):
	def __init__(self):
		super().__init__()
		self.models = { team: MLPClassifier() for team in self.training_data.keys()}
		self.model_name = "multi-perceptron"

	def train(self):
		for team, model in self.models.items():
			model.fit(np.array(self.training_data[team]['X']), np.array(self.training_data[team]['Y']))

	def predict(self, team, opponent):
		return self.models[team].predict(np.array([self.create_matchup_feature_vector(team, opponent)]))[0]
