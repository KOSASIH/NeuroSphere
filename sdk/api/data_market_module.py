import os
import logging
from flask_sqlalchemy import SQLAlchemy

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create SQLAlchemy instance
db = SQLAlchemy()

class DataMarket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(200), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }
class Dataset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data_market_id = db.Column(db.Integer, db.ForeignKey('data_market.id'))
    data_market = db.relationship('DataMarket', backref=db.backref('datasets', lazy=True))
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    data = db.Column(db.String, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'data': self.data
        }
class DataMarketModule:
    def __init__(self):
        self.data_markets = []

    def get_data_markets(self):
        return DataMarket.query.all()

    def get_data_market(self, data_market_id):
        return DataMarket.query.get(data_market_id)

    def create_data_market(self, name, description):
        data_market = DataMarket(name=name, description=description)
        db.session.add(data_market)
        db.session.commit()
        return data_market

    def update_data_market(self, data_market_id, name, description):
        data_market = DataMarket.query.get(data_market_id)
        if data_market is None:
            return None
        data_market.name = name
        data_market.description = description
        db.session.commit()
        return data_market

    def delete_data_market(self, data_market_id):
        data_market = DataMarket.query.get(data_market_id)
        if data_market is None:
            return
        db.session.delete(data_market)
        db.session.commit()

    def get_datasets(self, data_market_id):
        return Dataset.query.filter_by(data_market_id=data_market_id).all()

    def get_dataset(self, data_market_id, dataset_id):
        return Dataset.query.filter_by(data_market_id=data_market_id, id=dataset_id).first()

    def create_dataset(self, data_market_id, name, description, data):
        dataset = Dataset(data_market_id=data_market_id, name=name, description=description, data=data)
        db.session.add(dataset)
        db.session.commit()
        return dataset

    def update_dataset(self, data_market_id, dataset_id, name, description, data):
        dataset = Dataset.query.filter_by(data_market_id=data_market_id, id=dataset_id).first()
        if dataset is None:
            return None
        dataset.name = name
        dataset.description = description
        dataset.data = data
        db.session.commit()
        return dataset

    def delete_dataset(self, data_market_id, dataset_id):
        dataset = Dataset.query.filter_by(data_market_id=data_market_id, id=dataset_id).first()
        if dataset is None:
            return
        db.session.delete(dataset)
        db.session.commit()
