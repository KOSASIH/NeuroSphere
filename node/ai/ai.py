import numpy as np
import pandas as pd
from decision_making import DecisionMaker
from machine_learning import MachineLearner

class AI:
    def __init__(self, data, target):
        self.data = data
        self.target = target
        self.decision_maker = DecisionMaker(data, target)
        self.machine_learner = MachineLearner(data, target)

    def make_decision(self, input_data):
        return self.decision_maker.make_decision(input_data)

    def train_model(self, model_type):
        X_train, X_test, y_train, y_test = self.machine_learner.preprocess_data()
        if model_type == 'random_forest':
            self.machine_learner.train_random_forest(X_train, X_test, y_train, y_test)
        elif model_type == 'neural_network':
            self.machine_learner.train_neural_network(X_train, X_test, y_train, y_test)
        elif model_type == 'transformer':
            self.machine_learner.train_transformer(X_train, X_test, y_train, y_test)

    def evaluate_model(self, model_type):
        X_test, y_test = self.machine_learner.preprocess_data()[-2:]
        self.machine_learner.evaluate_model(X_test, y_test)

    def save_model(self, filename, model_type):
        self.machine_learner.save_model(filename, model_type)

    def load_model(self, filename, model_type):
        self.machine_learner.load_model(filename, model_type)
