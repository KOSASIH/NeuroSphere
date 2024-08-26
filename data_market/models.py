from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

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
