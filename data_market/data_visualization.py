import os
import logging
from flask import Flask, request, jsonify
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)

# Define API endpoints
@app.route("/api/datasets/<int:dataset_id>/visualize", methods=["POST"])
@jwt_required
def visualize_dataset(dataset_id):
    dataset = Dataset.query.get(dataset_id)
    if dataset is None:
        return jsonify({"error": "Dataset not found"}), 404
    data = dataset.data
    plt.figure(figsize=(10, 6))
    sns.countplot(x="category", data=data)
    plt.title("Category Distribution")
    plt.xlabel("Category")
    plt.ylabel("Count")
    img = BytesIO()
    plt.savefig(img, format="png")
    img.seek(0)
    return send_file(img, mimetype="image/png")

@app.route("/api/datasets/<int:dataset_id>/correlation", methods=["POST"])
@jwt_required
def correlation_matrix(dataset_id):
    dataset = Dataset.query.get(dataset_id)
    if dataset is None:
        return jsonify({"error": "Dataset not found"}), 404
    data = dataset.data
    corr_matrix = data.corr()
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap="coolwarm")
    plt.title("Correlation Matrix")
    img = BytesIO()
    plt.savefig(img, format="png")
    img.seek(0)
    return send_file(img, mimetype="image/png")

if __name__ == "__main__":
    app.run(debug=True)
