import os
import logging
from flask import Flask, request, jsonify
from blockchain import Blockchain

app = Flask(__name__)

blockchain = Blockchain()

@app.route("/mine", methods=["GET"])
def mine_block():
    blockchain.mine_block()
    return jsonify({"block": blockchain.last_block.to_dict()})

@app.route("/transactions", methods=["GET"])
def get_transactions():
    return jsonify([tx.to_dict() for tx in blockchain.transactions])

@app.route("/transactions", methods=["POST"])
def add_transaction():
    data = request.get_json()
    tx = blockchain.add_transaction(data["sender"], data["recipient"], data["amount"])
    return jsonify(tx.to_dict())

@app.route("/chain", methods=["GET"])
def get_chain():
    return jsonify([block.to_dict() for block in blockchain.chain])

if __name__ == "__main__":
    app.run(debug=True)
