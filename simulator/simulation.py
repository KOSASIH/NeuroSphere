import os
import sys
import time
import threading
import queue
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource
from flask_cors import CORS

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///simulation.db"
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)
cors = CORS(app)

class Simulation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(64), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "status": self.status
        }

class NodeSimulation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    simulation_id = db.Column(db.Integer, db.ForeignKey("simulation.id"))
    simulation = db.relationship("Simulation", backref=db.backref("node_simulations", lazy=True))
    node_id = db.Column(db.Integer, db.ForeignKey("node.id"))
    node = db.relationship("Node", backref=db.backref("node_simulations", lazy=True))
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(64), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "simulation_id": self.simulation_id,
            "node_id": self.node_id,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "status": self.status
        }

class Node(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    ip_address = db.Column(db.String(64), nullable=False)
    port = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "ip_address": self.ip_address,
            "port": self.port
        }

class SimulationSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "description", "start_time", "end_time", "status")

class NodeSimulationSchema(ma.Schema):
    class Meta:
        fields = ("id", "simulation_id", "node_id", "start_time", "end_time", "status")

class NodeSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "description", "ip_address", "port")

simulation_schema = SimulationSchema()
node_simulation_schema = NodeSimulationSchema()
node_schema = NodeSchema()

@app.route("/simulations", methods=["GET"])
def get_simulations():
    simulations = Simulation.query.all()
    return jsonify([simulation_schema.dump(simulation) for simulation in simulations])

@app.route("/simulations", methods=["POST"])
def create_simulation():
    data = request.get_json()
    simulation = Simulation(name=data["name"], description=data["description"], start_time=data["start_time"], end_time=data["end_time"], status=data["status"])
    db.session.add(simulation)
    db.session.commit()
    return jsonify(simulation_schema.dump(simulation))

@app.route("/simulations/<int:simulation_id>", methods=["GET"])
def get_simulation(simulation_id):
    simulation = Simulation.query.get(simulation_id)
    if simulation is None:
        return jsonify({"error": "Simulation not found"}), 404
    return jsonify(simulation_schema.dump(simulation))

@app.route("/node_simulations", methods=["GET"])
def get_node_simulations():
    node_simulations = NodeSimulation.query.all()
    return jsonify([node_simulation_schema.dump(node_simulation) for node_simulation in node_simulations])

@app.route("/node_simulations/<int:node_simulation_id>", methods=["GET"])
def get_node_simulation(node_simulation_id):
    node_simulation = NodeSimulation.query.get(node_simulation_id)
    if node_simulation is None:
        return jsonify({"error": "Node simulation not found"}), 404
    return jsonify(node_simulation_schema.dump(node_simulation))

@app.route("/nodes", methods=["GET"])
def get_nodes():
    nodes = Node.query.all()
    return jsonify([node_schema.dump(node) for node in nodes])

@app.route("/nodes", methods=["POST"])
def create_node():
    data = request.get_json()
    node = Node(name=data["name"], description=data["description"], ip_address=data["ip_address"], port=data["port"])
    db.session.add(node)
    db.session.commit()
    return jsonify(node_schema.dump(node))

@app.route("/nodes/<int:node_id>", methods=["GET"])
def get_node(node_id):
    node = Node.query.get(node_id)
    if node is None:
        return jsonify({"error": "Node not found"}), 404
    return jsonify(node_schema.dump(node))

def train_model(simulation_id):
    simulation = Simulation.query.get(simulation_id)
    if simulation is None:
        return
    X = []
    y = []
    for node_simulation in simulation.node_simulations:
        X.append(node_simulation.node.ip_address)
        y.append(node_simulation.status)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    return accuracy

def predict(simulation_id, ip_address):
    simulation = Simulation.query.get(simulation_id)
    if simulation is None:
        return
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.load("model.pkl")
    X = [ip_address]
    y_pred = model.predict(X)
    return y_pred[0]

if __name__ == "__main__":
    app.run(debug=True)
