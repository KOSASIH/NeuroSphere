import os
import logging
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URI"]
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Define models
class DataShare(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dataset_id = db.Column(db.Integer, db.ForeignKey("dataset.id"), nullable=False)
    dataset = db.relationship("Dataset", backref="shares")
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("User", backref="shares")
    permissions = db.Column(db.String(64), nullable=False, default="read")

class DataShareRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data_share_id = db.Column(db.Integer, db.ForeignKey("data_share.id"), nullable=False)
    data_share = db.relationship("DataShare", backref="requests")
    requester_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    requester = db.relationship("User", backref="requests")
    status = db.Column(db.String(64), nullable=False, default="pending")

# Define API endpoints
@app.route("/api/datasets/<int:dataset_id>/shares", methods=["POST"])
@jwt_required
def create_data_share(dataset_id):
    dataset = Dataset.query.get(dataset_id)
    if dataset is None:
        return jsonify({"error": "Dataset not found"}), 404
    user_id = request.json["user_id"]
    permissions = request.json["permissions"]
    data_share = DataShare(dataset_id=dataset_id, user_id=user_id, permissions=permissions)
    db.session.add(data_share)
    db.session.commit()
    return jsonify({"id": data_share.id})

@app.route("/api/data_shares/<int:data_share_id>/requests", methods=["POST"])
@jwt_required
def create_data_share_request(data_share_id):
    data_share = DataShare.query.get(data_share_id)
    if data_share is None:
        return jsonify({"error": "Data share not found"}), 404
    requester_id = get_jwt_identity()
    request = DataShareRequest(data_share_id=data_share_id, requester_id=requester_id)
    db.session.add(request)
    db.session.commit()
    return jsonify({"id": request.id})

@app.route("/api/data_share_requests/<int:request_id>", methods=["GET"])
@jwt_required
def get_data_share_request(request_id):
    request = DataShareRequest.query.get(request_id)
    if request is None:
        return jsonify({"error": "Request not found"}), 404
    return jsonify({"status": request.status})

@app.route("/api/data_share_requests/<int:request_id>/approve", methods=["POST"])
@jwt_required
def approve_data_share_request(request_id):
    request = DataShareRequest.query.get(request_id)
    if request is None:
        return jsonify({"error": "Request not found"}), 404
    request.status = "approved"
    db.session.commit()
    return jsonify({"status": request.status})

@app.route("/api/data_share_requests/<int:request_id>/reject", methods=["POST"])
@jwt_required
def reject_data_share_request(request_id):
    request = DataShareRequest.query.get(request_id)
    if request is None:
        return jsonify({"error": "Request not found"}), 404
    request.status = "rejected"
    db.session.commit()
    return jsonify({"status": request.status})

if __name__ == "__main__":
    app.run(debug=True)
