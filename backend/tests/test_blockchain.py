import pytest
from backend.blockchain.blockchain import Blockchain
from backend.blockchain.block import GENESIS_DATA


@pytest.fixture
def three_blocks():
    """
    Fixture that creates a blockchain with three blocks.

    Returns:
        Blockchain: A Blockchain instance with three blocks.
    """
    blockchain = Blockchain()
    for number in range(3):
        blockchain.add_block(number)
    return blockchain


def test_blockchain_instance():
    """
    Tests the instantiation of a Blockchain instance.
    """
    blackchin = Blockchain()

    assert blackchin.chain[0].hash == GENESIS_DATA["hash"]


def test_add_block():
    """
    Tests the add_block method of the Blockchain class.
    """
    blockchain = Blockchain()
    data = "test_data"
    blockchain.add_block(data)

    assert blockchain.chain[-1].data == data


def test_is_valid_chain(three_blocks):
    """
    Tests the is_valid_chain method of the Blockchain class.

    Args:
        three_blocks (Blockchain): A blockchain instance with three blocks.
    """
    Blockchain.is_valid_chain(three_blocks.chain)


def test_is_valid_chain_bad_genesis(three_blocks):
    """
    Tests the is_valid_chain method of the Blockchain class with a bad genesis block.

    Args:
        three_blocks (Blockchain): A blockchain instance with three blocks.
    """
    three_blocks.chain[0].hash = "bad_hash"
    with pytest.raises(Exception, match="The genesis block must be valid"):
        Blockchain.is_valid_chain(three_blocks.chain)


def tets_replace_chain(tree_blocks):
    """
    Tests the replace_chain method of the Blockchain class.

    Args:
        three_blocks (Blockchain): A blockchain instance with three blocks.
    """
    blockchain = Blockchain()
    blockchain.replace_chain(tree_blocks.chain)
    assert blockchain.chain == tree_blocks.chain


def test_replace_chain_not_longer(three_blocks):
    """
    Tests the replace_chain method of the Blockchain class with a shorter chain.

    Args:
        three_blocks (Blockchain): A blockchain instance with three blocks.
    """
    blockchain = Blockchain()
    with pytest.raises(Exception, match="The incoming chain must be longer."):
        three_blocks.replace_chain(blockchain.chain)


def test_replace_chain_bad_chain(three_blocks: Blockchain) -> None:
    """
    Tests the replace_chain method of the Blockchain class with a shorter chain.

    Args:
        three_blocks (Blockchain): A blockchain instance with three blocks.
    """
    blockchain = Blockchain()
    three_blocks.chain[0].hash = "bad_hash"
    with pytest.raises(Exception, match="The incoming chain is invalid"):
        blockchain.replace_chain(three_blocks.chain)
