import os
import random
import requests
from dotenv import load_dotenv
from flask import Flask, jsonify
from backend.blockchain.blockchain import Blockchain
from backend.pubsub import PubSub

load_dotenv()

app = Flask(__name__)
blockchain = Blockchain()
blockchain.add_block([])
blockchain.add_block([])
blockchain.add_block([])
pubsub = PubSub(blockchain)


@app.route("/")
def route_default():
    return "Welcome to blockchain."


@app.route("/blockchain")
def route_blockchain():
    return jsonify(blockchain.to_json())


@app.route("/blockchain/mine")
def route_blockchain_mine():
    transaction_data = "stubbed_transacion_data"
    blockchain.add_block(transaction_data)
    block = blockchain.chain[-1]
    pubsub.brodcats_block(block)
    return jsonify(blockchain.chain[-1].to_json())


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
