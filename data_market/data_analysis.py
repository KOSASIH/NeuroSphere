import os
import logging
from flask import Flask, request, jsonify
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)

# Define API endpoints
@app.route("/api/datasets/<int:dataset_id>/analyze", methods=["POST"])
@jwt_required
def analyze_dataset(dataset_id):
    dataset = Dataset.query.get(dataset_id)
    if dataset is None:
        return jsonify({"error": "Dataset not found"}), 404
    data = dataset.data
    X = data.drop(["target"], axis=1)
    y = data["target"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    return jsonify({"mse": mse})

if __name__ == "__main__":
    app.run(debug=True)
