import os
import logging
import pandas as pd
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Model training class
class ModelTraining:
    def __init__(self, data_path: str, model_path: str):
        self.data_path = data_path
        self.model_path = model_path

    def load_data(self):
        data = pd.read_csv(self.data_path)
        X = data.drop(['label'], axis=1)
        y = data['label']
        return X, y

    def train_model(self, X: pd.DataFrame, y: pd.Series):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = Sequential()
        model.add(Dense(64, activation='relu', input_shape=(X.shape[1],)))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(1, activation='sigmoid'))
        model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
        model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test))
        model.save(self.model_path)
        logger.info(f'Trained model and saved to {self.model_path}')

if __name__ == '__main__':
    data_path = os.environ['DATA_PATH']
    model_path = os.environ['MODEL_PATH']
    model_training = ModelTraining(data_path, model_path)
    X, y = model_training.load_data()
    model_training.train_model(X, y)
