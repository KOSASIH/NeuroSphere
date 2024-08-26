import os
import logging
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from node_module import Node, NodeModule

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///node.db"
db = SQLAlchemy(app)

node_module = NodeModule()

@app.route("/nodes", methods=["GET"])
def get_nodes():
    nodes = node_module.get_nodes()
    return jsonify([node.to_dict() for node in nodes])

@app.route("/nodes", methods=["POST"])
def create_node():
    data = request.get_json()
    node = node_module.create_node(data["name"], data["description"], data["ip_address"], data["port"])
    return jsonify(node.to_dict()), 201

@app.route("/nodes/<int:node_id>", methods=["GET"])
def get_node(node_id):
    node = node_module.get_node(node_id)
    if node is None:
        return jsonify({"error": "Node not found"}), 404
    return jsonify(node.to_dict())

@app.route("/nodes/<int:node_id>", methods=["PUT"])
def update_node(node_id):
    data = request.get_json()
    node = node_module.update_node(node_id, data["name"], data["description"], data["ip_address"], data["port"])
    if node is None:
        return jsonify({"error": "Node not found"}), 404
    return jsonify(node.to_dict())

@app.route("/nodes/<int:node_id>", methods=["DELETE"])
def delete_node(node_id):
    node_module.delete_node(node_id)
    return jsonify({"message": "Node deleted"}), 204

if __name__ == "__main__":
    app.run(debug=True)
