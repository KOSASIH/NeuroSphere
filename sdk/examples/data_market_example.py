import os
import logging
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from data_market_module import DataMarket, Dataset, DataMarketModule

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data_market.db"
db = SQLAlchemy(app)

data_market_module = DataMarketModule()

@app.route("/data_markets", methods=["GET"])
def get_data_markets():
    data_markets = data_market_module.get_data_markets()
    return jsonify([data_market.to_dict() for data_market in data_markets])

@app.route("/data_markets", methods=["POST"])
def create_data_market():
    data = request.get_json()
    data_market = data_market_module.create_data_market(data["name"], data["description"])
    return jsonify(data_market.to_dict()), 201

@app.route("/data_markets/<int:data_market_id>", methods=["GET"])
def get_data_market(data_market_id):
    data_market = data_market_module.get_data_market(data_market_id)
    if data_market is None:
        return jsonify({"error": "Data market not found"}), 404
    return jsonify(data_market.to_dict())

@app.route("/data_markets/<int:data_market_id>", methods=["PUT"])
def update_data_market(data_market_id):
    data = request.get_json()
    data_market = data_market_module.update_data_market(data_market_id, data["name"], data["description"])
    if data_market is None:
        return jsonify({"error": "Data market not found"}), 404
    return jsonify(data_market.to_dict())

@app.route("/data_markets/<int:data_market_id>", methods=["DELETE"])
def delete_data_market(data_market_id):
    data_market_module.delete_data_market(data_market_id)
    return jsonify({"message": "Data market deleted"}), 204

@app.route("/data_markets/<int:data_market_id>/datasets", methods=["GET"])
def get_datasets(data_market_id):
    datasets = data_market_module.get_datasets(data_market_id)
    return jsonify([dataset.to_dict() for dataset in datasets])

@app.route("/data_markets/<int:data_market_id>/datasets", methods=["POST"])
def create_dataset(data_market_id):
    data = request.get_json()
    dataset = data_market_module.create_dataset(data_market_id, data["name"], data["description"], data["data"])
    return jsonify(dataset.to_dict()), 201

@app.route("/data_markets/<int:data_market_id>/datasets/<int:dataset_id>", methods=["GET"])
def get_dataset(data_market_id, dataset_id):
    dataset = data_market_module.get_dataset(data_market_id, dataset_id)
    if dataset is None:
        return jsonify({"error": "Dataset not found"}), 404
    return jsonify(dataset.to_dict())

@app.route("/data_markets/<int:data_market_id>/datasets/<int:dataset_id>", methods=["PUT"])
def update_dataset(data_market_id, dataset_id):
    data = request.get_json()
    dataset = data_market_module.update_dataset(data_market_id, dataset_id, data["name"], data["description"], data["data"])
    if dataset is None:
        return jsonify({"error": "Dataset not found"}), 404
    return jsonify(dataset.to_dict())

@app.route("/data_markets/<int:data_market_id>/datasets/<int:dataset_id>", methods=["DELETE"])
def delete_dataset(data_market_id, dataset_id):
    data_market_module.delete_dataset(data_market_id, dataset_id)
    return jsonify({"message": "Dataset deleted"}), 204

if __name__ == "__main__":
    app.run(debug=True)
