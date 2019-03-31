from sklearn.tree import DecisionTreeClassifier
import numpy as np
import warnings

from matchup_model import MatchupModel

warnings.filterwarnings("ignore")

class MMDecisionTree(MatchupModel):
	def __init__(self):
		super().__init__()
		self.models = { team: DecisionTreeClassifier() for team in self.training_data.keys()}
		self.model_name = "decision-tree"
