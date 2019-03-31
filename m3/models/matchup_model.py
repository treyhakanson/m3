import pandas as pd 
import numpy as np 
import json
import os 

from model import Model

class MockModel():
  def fit(self, X, Y):
  	# Fits model to data X, Y 
    pass

  def predict(self, feature_vectors):
  	# Returns 0 or 1 for each feature vector 
    return [1 for _ in feature_vectors]

class MatchupModel(Model):
  '''
  Creates a model that uses player matchup data as a feature vector. 
  Provides attributes...
  self.training_data = {
    team: {
      X: [0, 1, ...]
      Y: [
        [feature1, feature2, ...],
        [feature1, feature2, ...], 
        ...
      ]
    }
  }
  self.feature_vectors = {
    team: [feature1, feature2, ...]
  }
  self.models = {
		team: model matching MockModel attributes 
  }
  ...and methods for creating feature vectors, training, and predicting 
  '''
  def __init__(self, data='binary'):
    super().__init__()
    fname = './cleaned-data/%s-data.json' % ('binary' if data=='binary' else 'point-ratio')
    with open(fname, 'r') as f:
      self.training_data = json.loads(f.read())
    self.feature_vectors = self.import_feature_vectors()
    self.models = { team: MockModel() for team in self.training_data.keys()}


  def import_feature_vectors(self):
    FEATURE_DIR = './feature-vectors'
    feature_vectors = {}
    for fname in os.listdir(FEATURE_DIR):
      if fname.endswith(".csv"):
        teamname = fname.replace('.csv', '')
        feature_vect = pd.read_csv(os.path.join(FEATURE_DIR, fname), index_col=0).values.flatten().tolist()
        feature_vectors[teamname] = feature_vect
    return feature_vectors

  def create_matchup_feature_vector(self, team, opponent):
    return self.feature_vectors[team] + self.feature_vectors[opponent]

  def train(self):
    for team, model in self.models.items():
      model.fit(np.array(self.training_data[team]['X']), np.array(self.training_data[team]['Y']))

  def predict(self, team, opponent):
    return self.models[team].predict(np.array([self.create_matchup_feature_vector(team, opponent)]))[0]
