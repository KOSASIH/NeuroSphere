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

