"""Container for the application."""

import os
import random

import requests
from flask import Flask, Response, jsonify, request
from flask_cors import CORS

from backend.blockchain.blockchain import Blockchain
from backend.pubsub import PubSub
from backend.wallet.transaction import Transaction
from backend.wallet.transaction_pool import TransactionPool
from backend.wallet.wallet import Wallet

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
blockchain = Blockchain()
wallet = Wallet(blockchain)
transaction_pool = TransactionPool()
pubsub = PubSub(blockchain, transaction_pool)


@app.route("/")  # type: ignore
def route_default() -> str:
    """
    Default route handler for the Flask application.

    Returns:
        str: Welcome message.
    """
    return "Welcome to blockchain."


@app.route("/blockchain")  # type: ignore
def route_blockchain() -> Response:
    """
    Route handler for retrieving the state of the blockchain.

    Returns:
        Response: A JSON object representing the state of the blockchain.
    """
    return jsonify(blockchain.to_json())


@app.route("/blockchain/mine")  # type: ignore
def route_blockchain_mine() -> Response:
    """
    Route handler for mining a new block in the blockchain.

    Returns:
        Response: A JSON object representing the new block.
    """
    transaction_data = "stubbed_transaction_data"
    blockchain.add_block(transaction_data)
    block = blockchain.chain[-1]
    pubsub.broadcast_block(block)
    return jsonify(block.to_json())


@app.route("/wallet/transact", methods=["POST"])
def route_wallet_transact() -> Response:
    transaction_data = request.get_json()
    transaction = transaction_pool.existing_transaction(wallet.address)

    if transaction:
        transaction.update(wallet, transaction_data["recipient"], transaction_data["amount"])
    else:
        transaction = Transaction(wallet, transaction_data["recipient"], transaction_data["amount"])

    pubsub.broadcast_transaction(transaction)
    transaction_pool.set_transaction(transaction)

    return jsonify(transaction.to_json())


ROOT_PORT = 5000
PORT = ROOT_PORT

if os.environ.get("PEER") == "True":
    PORT = random.randint(5001, 6000)

    result = requests.get(f"http://localhost:{ROOT_PORT}/blockchain")
    result_blockchain = Blockchain.from_json(result.json())

    try:
        blockchain.replace_chain(result_blockchain.chain)
        print("\n -- Successfully synchronized the local chain")
    except Exception as e:
        print(f"\n -- Error synchronizing: {e}")


app.run(port=PORT)
