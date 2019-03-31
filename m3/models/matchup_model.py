import pandas as pd 
import json
import os 

from model import Model

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
  ...and a helper method to create a concatenated feature vector for two teams
  '''
  def __init__(self, data='binary'):
    super().__init__()
    fname = './cleaned-data/%s-data.json' % ('binary' if data=='binary' else 'point-ratio')
    with open(fname, 'r') as f:
      self.training_data = json.loads(f.read())
    self.feature_vectors = self.import_feature_vectors()

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
