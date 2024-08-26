import os
import logging
from flask import jsonify

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def error_response(error_message, status_code):
    return jsonify({"error": error_message}), status_code

def success_response(data, status_code):
    return jsonify({"data": data}), status_code
