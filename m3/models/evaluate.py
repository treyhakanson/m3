from .model import Model
from .perceptron import MMPerceptron

if __name__ == '__main__':
    print('======Base Model======')
    model = Model()
    model.train()
    model.test()

    print()

    print('======Perceptron======')
    perceptron = MMPerceptron()
    perceptron.train()
    perceptron.test()
