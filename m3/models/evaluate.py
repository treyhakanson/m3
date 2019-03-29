import sys

from .model import Model
from .perceptron import MMPerceptron

if __name__ == '__main__':
    model_choice = 'all' if len(sys.argv) < 2 else sys.argv[1].lower()

    if (model_choice == 'all' or model_choice == 'model'):
        print('======Base Model======')
        model = Model()
        model.train()
        model.test()
        print()

    if (model_choice == 'all' or model_choice == 'perceptron'):
        print('======Perceptron======')
        perceptron = MMPerceptron()
        perceptron.train()
        perceptron.test()
