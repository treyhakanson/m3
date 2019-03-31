from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.neural_network import MLPRegressor
import numpy as np
import warnings

from matchup_model import MatchupModel

warnings.filterwarnings("ignore")

class MMLinearRegression(MatchupModel):
	def __init__(self):
		super().__init__(data='point-ratio')
		self.models = { team: LinearRegression() for team in self.training_data.keys()}
		self.model_name = "linear-regression"

class MMLogisticRegression(MatchupModel):
	def __init__(self):
		super().__init__()
		self.models = { team: LogisticRegression() for team in self.training_data.keys()}
		self.model_name = "logistic-regression"

class MMMultilayerRegression(MatchupModel):
	def __init__(self):
		super().__init__(data='point-ratio')
		self.models = { team: MLPRegressor() for team in self.training_data.keys()}
		self.model_name = "multi-regression"
