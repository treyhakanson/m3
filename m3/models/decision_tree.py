from sklearn.tree import DecisionTreeClassifier
import numpy as np
import warnings

from matchup_model import MatchupModel

warnings.filterwarnings("ignore")

class MMDecisionTree(MatchupModel):
	def __init__(self):
		super().__init__()
		self.models = { team: DecisionTreeClassifier() for team in self.training_data.keys()}
		self.model_name = "linear-regression"

	def train(self):
		for team, model in self.models.items():
			model.fit(np.array(self.training_data[team]['X']), np.array(self.training_data[team]['Y']))

	def predict(self, team, opponent):
		return self.models[team].predict(np.array([self.create_matchup_feature_vector(team, opponent)]))[0]
