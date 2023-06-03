from backend.blockchain.blockchain import Blockchain
from backend.config import STARTING_BALANCE
from backend.wallet.transaction import Transaction
from backend.wallet.wallet import Wallet


def test_verify_valid_signature():
    data = {"foo": "test_data"}
    wallet = Wallet()
    signatire = wallet.sign(data)
    assert Wallet.verify(wallet.public_key, data, signatire)


def test_verify_invalid_signature():
    data = {"foo": "test_data"}
    wallet = Wallet()
    signatire = wallet.sign(data)
    assert not Wallet.verify(Wallet().public_key, data, signatire)


def test_calculate_balance():
    blockchain = Blockchain()
    wallet = Wallet()

    assert Wallet.calculate_balance(blockchain, wallet.address) == STARTING_BALANCE

    amount = 50
    transaction = Transaction(wallet, "recipient", amount)
    blockchain.add_block([transaction.to_json()])

    assert Wallet.calculate_balance(blockchain, wallet.address) == STARTING_BALANCE - amount
