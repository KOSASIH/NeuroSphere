import os
import logging
from flask import Flask, request, jsonify
from flask_restplus import Api, Resource, fields
from data_market_module import DataMarketModule

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)
api = Api(app, version='1.0', title='Data Market API', description='Advanced Data Market API')

# Define API namespace
ns = api.namespace('data_market', description='Data market operations')

# Define DataMarket model
data_market_model = api.model('DataMarket', {
    'id': fields.Integer(readOnly=True, description='The data market ID'),
    'name': fields.String(required=True, description='The data market name'),
    'description': fields.String(description='The data market description'),
    ' datasets': fields.List(fields.Nested(api.model('Dataset', {
        'id': fields.Integer(readOnly=True, description='The dataset ID'),
        'name': fields.String(required=True, description='The dataset name'),
        'description': fields.String(description='The dataset description'),
        'data': fields.String(required=True, description='The dataset data')
    })))
})

# Define DataMarketModule instance
data_market_module = DataMarketModule()

# Define API endpoints
@ns.route('/')
class DataMarketList(Resource):
    def get(self):
        data_markets = data_market_module.get_data_markets()
        return {'data_markets': [data_market.to_dict() for data_market in data_markets]}

    def post(self):
        data = request.get_json()
        data_market = data_market_module.create_data_market(data['name'], data['description'])
        return {'data_market': data_market.to_dict()}, 201

@ns.route('/<int:data_market_id>')
class DataMarket(Resource):
    def get(self, data_market_id):
        data_market = data_market_module.get_data_market(data_market_id)
        if data_market is None:
            return {'error': 'Data market not found'}, 404
        return {'data_market': data_market.to_dict()}

    def put(self, data_market_id):
        data = request.get_json()
        data_market = data_market_module.update_data_market(data_market_id, data['name'], data['description'])
        return {'data_market': data_market.to_dict()}

    def delete(self, data_market_id):
        data_market_module.delete_data_market(data_market_id)
        return '', 204

@ns.route('/<int:data_market_id>/datasets')
class DatasetList(Resource):
    def get(self, data_market_id):
        datasets = data_market_module.get_datasets(data_market_id)
        return {'datasets': [dataset.to_dict() for dataset in datasets]}

    def post(self, data_market_id):
        data = request.get_json()
        dataset = data_market_module.create_dataset(data_market_id, data['name'], data['description'], data['data'])
        return {'dataset': dataset.to_dict()}, 201

@ns.route('/<int:data_market_id>/datasets/<int:dataset_id>')
class Dataset(Resource):
    def get(self, data_market_id, dataset_id):
        dataset = data_market_module.get_dataset(data_market_id, dataset_id)
        if dataset is None:
            return {'error': 'Dataset not found'}, 404
        return {'dataset': dataset.to_dict()}

    def put(self, data_market_id, dataset_id):
        data = request.get_json()
        dataset = data_market_module.update_dataset(data_market_id, dataset_id, data['name'], data['description'], data['data'])
        return {'dataset': dataset.to_dict()}

    def delete(self, data_market_id, dataset_id):
        data_market_module.delete_dataset(data_market_id, dataset_id)
        return '', 204

if __name__ == '__main__':
    app.run(debug=True)
