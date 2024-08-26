import os
import logging
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager, jwt_required, create_access_token

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URI"]
app.config["JWT_SECRET_KEY"] = os.environ["JWT_SECRET_KEY"]
db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)

# Define models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

class Dataset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    data = db.Column(db.LargeBinary, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    owner = db.relationship("User", backref="datasets")

class DataRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dataset_id = db.Column(db.Integer, db.ForeignKey("dataset.id"), nullable=False)
    dataset = db.relationship("Dataset", backref="requests")
    requester_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    requester = db.relationship("User", backref="requests")
    status = db.Column(db.String(64), nullable=False, default="pending")

# Define API endpoints
@app.route("/api/users", methods=["POST"])
def create_user():
    username = request.json["username"]
    email = request.json["email"]
    user = User(username=username, email=email)
    db.session.add(user)
    db.session.commit()
    return jsonify({"id": user.id})

@app.route("/api/datasets", methods=["POST"])
@jwt_required
def create_dataset():
    name = request.json["name"]
    description = request.json["description"]
    data = request.json["data"]
    dataset = Dataset(name=name, description=description, data=data, owner_id=get_jwt_identity())
    db.session.add(dataset)
    db.session.commit()
    return jsonify({"id": dataset.id})

@app.route("/api/datasets/<int:dataset_id>/requests", methods=["POST"])
@jwt_required
def create_data_request(dataset_id):
    dataset = Dataset.query.get(dataset_id)
    if dataset is None:
        return jsonify({"error": "Dataset not found"}), 404
    requester_id = get_jwt_identity()
    request = DataRequest(dataset_id=dataset_id, requester_id=requester_id)
    db.session.add(request)
    db.session.commit()
    return jsonify({"id": request.id})

@app.route("/api/data_requests/<int:request_id>", methods=["GET"])
@jwt_required
def get_data_request(request_id):
    request = DataRequest.query.get(request_id)
    if request is None:
        return jsonify({"error": "Request not found"}), 404
    return jsonify({"status": request.status})

@app.route("/api/data_requests/<int:request_id>/approve", methods=["POST"])
@jwt_required
def approve_data_request(request_id):
    request = DataRequest.query.get(request_id)
    if request is None:
        return jsonify({"error": "Request not found"}), 404
    request.status = "approved"
    db.session.commit()
    return jsonify({"status": request.status})

@app.route("/api/data_requests/<int:request_id>/reject", methods=["POST"])
@jwt_required
def reject_data_request(request_id):
    request = DataRequest.query.get(request_id)
    if request is None:
        return jsonify({"error": "Request not found"}), 404
    request.status = "rejected"
    db.session.commit()
    return jsonify({"status": request.status})

if __name__ == "__main__":
    app.run(debug=True)
