import sys

from model import Model
from perceptron import MMPerceptron, MMMultilayerPerceptron
from regression import MMLogisticRegression, MMLinearRegression, MMMultilayerRegression
from decision_tree import MMDecisionTree

if __name__ == '__main__':
    model_choice = 'all' if len(sys.argv) < 2 else sys.argv[1].lower()

    if (model_choice == 'all' or model_choice == 'model'):
        print('\n======Base Model======')
        model = Model()
        model.train()
        model.test()

    if (model_choice == 'all' or model_choice == 'perceptron'):
        print('\n======Perceptron======')
        perceptron = MMPerceptron()
        perceptron.train()
        perceptron.test()

    if (model_choice == 'all' or model_choice == 'multi-perceptron'):
        print('\n======Multilayer Perceptron======')
        perceptron = MMMultilayerPerceptron()
        perceptron.train()
        perceptron.test()

    if (model_choice == 'all' or model_choice == 'logistic-regression'):
        print('\n======Logistic Regression======')
        perceptron = MMLogisticRegression()
        perceptron.train()
        perceptron.test()

    if (model_choice == 'all' or model_choice == 'linear-regression'):
        print('\n======Linear Regression======')
        perceptron = MMLinearRegression()
        perceptron.train()
        perceptron.test()

    if (model_choice == 'all' or model_choice == 'multi-regression'):
        print('\n======Multilayer Regression======')
        perceptron = MMMultilayerRegression()
        perceptron.train()
        perceptron.test()

    if (model_choice == 'all' or model_choice == 'decision-tree'):
        print('\n======Decision Tree======')
        perceptron = MMDecisionTree()
        perceptron.train()
        perceptron.test()