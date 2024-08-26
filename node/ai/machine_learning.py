import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.utils import to_categorical
from keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.optimizers import Adam
from transformers import AutoModelForSequenceClassification, AutoTokenizer

class MachineLearner:
    def __init__(self, data, target, model_type='random_forest'):
        self.data = data
        self.target = target
        self.model_type = model_type
        self.model = None
        self.scaler = StandardScaler()

    def preprocess_data(self):
        self.data = pd.get_dummies(self.data, drop_first=True)
        X = self.data.drop(self.target, axis=1)
        y = self.data[self.target]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        return X_train_scaled, X_test_scaled, y_train, y_test

    def train_random_forest(self, X_train, X_test, y_train, y_test):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model.fit(X_train, y_train)
        y_pred = self.model.predict(X_test)
        print("Random Forest Accuracy:", accuracy_score(y_test, y_pred))
        print("Random Forest Classification Report:")
        print(classification_report(y_test, y_pred))
        print("Random Forest Confusion Matrix:")
        print(confusion_matrix(y_test, y_pred))

    def train_neural_network(self, X_train, X_test, y_train, y_test):
        self.model = Sequential()
        self.model.add(Dense(64, activation='relu', input_shape=(X_train.shape[1],)))
        self.model.add(Dropout(0.2))
        self.model.add(Dense(32, activation='relu'))
        self.model.add(Dropout(0.2))
        self.model.add(Dense(8, activation='softmax'))
        self.model.compile(loss='categorical_crossentropy', optimizer=Adam(lr=0.001), metrics=['accuracy'])
        early_stopping = EarlyStopping(monitor='val_loss', patience=5, min_delta=0.001)
        model_checkpoint = ModelCheckpoint('best_model.h5', monitor='val_loss', save_best_only=True, mode='min')
        self.model.fit(X_train, to_categorical(y_train), epochs=50, batch_size=32, validation_data=(X_test, to_categorical(y_test)), callbacks=[early_stopping, model_checkpoint])
        y_pred = self.model.predict(X_test)
        print("Neural Network Accuracy:", accuracy_score(y_test, np.argmax(y_pred, axis=1)))
        print("Neural Network Classification Report:")
        print(classification_report(y_test, np.argmax(y_pred, axis=1)))
        print("Neural Network Confusion Matrix:")
        print(confusion_matrix(y_test, np.argmax(y_pred, axis=1)))

    def train_transformer(self, X_train, X_test, y_train, y_test):
        tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')
        X_train_tokenized = tokenizer.batch_encode_plus(X_train, max_length=512, padding='max_length', truncation=True)
        X_test_tokenized = tokenizer.batch_encode_plus(X_test, max_length=512, padding='max_length', truncation=True)
        self.model = AutoModelForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=8)
        self.model.fit(X_train_tokenized, y_train, epochs=5, batch_size=32, validation_data=(X_test_tokenized, y_test))
        y_pred = self.model.predict(X_test_tokenized)
        print("Transformer Accuracy:", accuracy_score(y_test, np.argmax(y_pred, axis=1)))
        print("Transformer Classification Report:")
        print(classification_report(y_test, np.argmax(y_pred, axis=1)))
        print("Transformer Confusion Matrix:")
        print(confusion_matrix(y_test, np.argmax(y_pred, axis=1)))

    def make_prediction(self, input_data):
        if self.model_type == 'random_forest':
            input_data_scaled = self.scaler.transform(input_data)
            return self.model.predict(input_data_scaled)
        elif self.model_type == 'neural_network':
            input_data_scaled = self.scaler.transform(input_data)
            return self.model.predict(input_data_scaled)
        elif self.model_type == 'transformer':
            input_data_tokenized = tokenizer.batch_encode_plus(input_data, max_length=512, padding='max_length', truncation=True)
            return self.model.predict(input_data_tokenized)

    def evaluate_model(self, X_test, y_test):
        if self.model_type == 'random_forest':
            y_pred = self.model.predict(X_test)
            print("Random Forest Accuracy:", accuracy_score(y_test, y_pred))
            print("Random Forest Classification Report:")
            print(classification_report(y_test, y_pred))
            print("Random Forest Confusion Matrix:")
            print(confusion_matrix(y_test, y_pred))
        elif self.model_type == 'neural_network':
            y_pred = self.model.predict(X_test)
            print("Neural Network Accuracy:", accuracy_score(y_test, np.argmax(y_pred, axis=1)))
            print("Neural Network Classification Report:")
            print(classification_report(y_test, np.argmax(y_pred, axis=1)))
            print("Neural Network Confusion Matrix:")
            print(confusion_matrix(y_test, np.argmax(y_pred, axis=1)))
        elif self.model_type == 'transformer':
            y_pred = self.model.predict(X_test)
            print("Transformer Accuracy:", accuracy_score(y_test, np.argmax(y_pred, axis=1)))
            print("Transformer Classification Report:")
            print(classification_report(y_test, np.argmax(y_pred, axis=1)))
            print("Transformer Confusion Matrix:")
            print(confusion_matrix(y_test, np.argmax(y_pred, axis=1)))

    def save_model(self, filename):
        if self.model_type == 'random_forest':
            joblib.dump(self.model, filename)
        elif self.model_type == 'neural_network':
            self.model.save(filename)
        elif self.model_type == 'transformer':
            self.model.save_pretrained(filename)

    def load_model(self, filename):
        if self.model_type == 'random_forest':
            self.model = joblib.load(filename)
        elif self.model_type == 'neural_network':
            self.model = load_model(filename)
        elif self.model_type == 'transformer':
            self.model = AutoModelForSequenceClassification.from_pretrained(filename)
