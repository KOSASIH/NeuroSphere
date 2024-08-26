import asyncio
import json
import os
import random
import time
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes

class Network:
    def __init__(self):
        self.nodes = {}
        self.node_ids = set()

    async def connect(self, node):
        node_id = node.node_id
        self.nodes[node_id] = node
        self.node_ids.add(node_id)
        await self.broadcast_node(node_id, node.public_key)

        async def broadcast_node(self, node_id, public_key):
        for node in self.nodes.values():
            if node.node_id != node_id:
                await node.connect_peer(node_id, public_key)

    async def send(self, node_id, message):
        node = self.nodes[node_id]
        return await node.handle_message(message)

    async def handle_message(self, node_id, message):
        node = self.nodes[node_id]
        if message['type'] == 'add_block':
            await node.add_block(message['block'])
        elif message['type'] == 'add_transaction':
            await node.add_transaction(message['transaction'])
        elif message['type'] == 'get_blockchain':
            return await node.get_blockchain()
        elif message['type'] == 'get_transaction_pool':
            return await node.get_transaction_pool()
        elif message['type'] == 'get_peers':
            return await node.get_peers()

    async def start(self):
        while True:
            await asyncio.sleep(1)

# Example usage:
network = Network()
node1 = Node('node1', rsa.generate_private_key(public_exponent=65537, key_size=2048), network)
node2 = Node('node2', rsa.generate_private_key(public_exponent=65537, key_size=2048), network)
node3 = Node('node3', rsa.generate_private_key(public_exponent=65537, key_size=2048), network)

async def main():
    await network.connect(node1)
    await network.connect(node2)
    await network.connect(node3)
    await network.start()

asyncio.run(main())
