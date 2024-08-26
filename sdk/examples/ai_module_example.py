import os
import logging
from flask import Flask, request, jsonify
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

app = Flask(__name__)

@app.route("/train", methods=["POST"])
def train_model():
    data = request.get_json()
    X = data["X"]
    y = data["y"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    return jsonify({"accuracy": accuracy})

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    X = data["X"]
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.load("model.pkl")
    y_pred = model.predict(X)
    return jsonify({"y_pred": y_pred.tolist()})

if __name__ == "__main__":
    app.run(debug=True)
