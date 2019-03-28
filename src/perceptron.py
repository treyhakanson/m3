from sklearn.linear_model import Perceptron
import numpy as np
import json 
import warnings

warnings.filterwarnings("ignore")

def get_training_data():
	with open('../cleaned-data/binary-data.json', 'r') as f:
		return json.loads(f.read())

def main():
	data = get_training_data()
	models = { team: Perceptron(random_state=0, max_iter=10) for team in data.keys()}
	for team, model in models.items():
		model.fit(np.array(data[team]['X']), np.array(data[team]['Y']))

main()
