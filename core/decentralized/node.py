import asyncio
import hashlib
import json
import os
import random
import time
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class Node:
    def __init__(self, node_id, private_key, public_key, network):
        self.node_id = node_id
        self.private_key = private_key
        self.public_key = public_key
        self.network = network
        self.peers = {}
        self.blockchain = []
        self.transaction_pool = []
        self.mining_difficulty = 1000

    async def start(self):
        await self.network.connect(self)
        await self.sync_blockchain()
        await self.start_mining()

    async def sync_blockchain(self):
        for peer in self.peers.values():
            blockchain = await peer.get_blockchain()
            if len(blockchain) > len(self.blockchain):
                self.blockchain = blockchain

    async def start_mining(self):
        while True:
            await self.mine_block()
            await asyncio.sleep(1)

    async def mine_block(self):
        transactions = self.transaction_pool[:10]
        self.transaction_pool = self.transaction_pool[10:]
        block = {
            'transactions': transactions,
            'previous_hash': self.blockchain[-1]['hash'] if self.blockchain else '0' * 64,
            'nonce': random.randint(0, 2**32 - 1)
        }
        block_hash = self.calculate_block_hash(block)
        while int(block_hash, 16) > self.mining_difficulty:
            block['nonce'] += 1
            block_hash = self.calculate_block_hash(block)
        self.blockchain.append(block)
        await self.broadcast_block(block)

    async def broadcast_block(self, block):
        for peer in self.peers.values():
            await peer.add_block(block)

    async def add_block(self, block):
        if self.validate_block(block):
            self.blockchain.append(block)
            await self.sync_blockchain()

    def calculate_block_hash(self, block):
        block_json = json.dumps(block, sort_keys=True)
        return hashlib.sha256(block_json.encode()).hexdigest()

    def validate_block(self, block):
        previous_hash = self.blockchain[-1]['hash'] if self.blockchain else '0' * 64
        if block['previous_hash'] != previous_hash:
            return False
        block_hash = self.calculate_block_hash(block)
        if int(block_hash, 16) > self.mining_difficulty:
            return False
        return True

    async def add_transaction(self, transaction):
        self.transaction_pool.append(transaction)
        await self.broadcast_transaction(transaction)

    async def broadcast_transaction(self, transaction):
        for peer in self.peers.values():
            await peer.add_transaction(transaction)

    async def get_blockchain(self):
        return self.blockchain

    async def get_transaction_pool(self):
        return self.transaction_pool

    async def get_peers(self):
        return list(self.peers.keys())

    async def connect_peer(self, node_id, public_key):
        self.peers[node_id] = NodeConnection(node_id, public_key, self.network)

class NodeConnection:
    def __init__(self, node_id, public_key, network):
        self.node_id = node_id
        self.public_key = public_key
        self.network = network

    async def add_block(self, block):
        await self.network.send(self.node_id, {'type': 'add_block', 'block': block})

    async def add_transaction(self, transaction):
        await self.network.send(self.node_id, {'type': 'add_transaction', 'transaction': transaction})

    async def get_blockchain(self):
        return await self.network.send(self.node_id, {'type': 'get_blockchain'})

    async def get_transaction_pool(self):
        return await self.network.send(self.node_id, {'type': 'get_transaction_pool'})

    async def get_peers(self):
        return await self.network.send(self.node_id, {'type': 'get_peers'})
