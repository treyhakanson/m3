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

class MMMultilayerPerceptron(MatchupModel):
	def __init__(self):
		super().__init__()
		self.models = { team: MLPClassifier() for team in self.training_data.keys()}
		self.model_name = "multi-perceptron"
