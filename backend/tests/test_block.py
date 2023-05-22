import time

import pytest

from backend.blockchain.block import GENESIS_DATA, Block
from backend.config import MINE_RATE, SECONDS
from backend.utils.hex_to_binary import hex_to_binary


def test_mine_block() -> None:
    """
    Tests the mine_block method of the Block class.
    """
    last_block = Block.genesis()
    data = "test-data"
    block = Block.mine_block(last_block, data)

    assert isinstance(block, Block)
    assert block.data == data
    assert block.last_hash == last_block.hash
    assert hex_to_binary(block.hash)[0 : block.difficulty] == "0" * block.difficulty


def test_genesis() -> None:
    """
    Tests the genesis method of the Block class.
    """
    genesis = Block.genesis()

    assert isinstance(genesis, Block)
    for key, value in GENESIS_DATA.items():
        getattr(genesis, key) == value


def test_quickly_mined_block() -> None:
    """
    Tests the difficulty adjustment for quickly mined blocks.
    """
    last_block = Block.mine_block(Block.genesis(), "foo")
    mined_block = Block.mine_block(last_block, "bar")

    assert mined_block.difficulty == last_block.difficulty + 1


def test_slowly_mined_block() -> None:
    """
    Tests the difficulty adjustment for slowly mined blocks.
    """
    last_block = Block.mine_block(Block.genesis(), "foo")
    time.sleep(MINE_RATE / SECONDS)
    mined_block = Block.mine_block(last_block, "bar")

    assert mined_block.difficulty == last_block.difficulty - 1


def test_mined_block_difficulty_limits_at_1() -> None:
    """
    Tests that the difficulty of mined blocks cannot go below 1.
    """
    last_block = Block(time.time_ns(), "test_last_hash", "test_hash", "test_data", 1, 0)

    time.sleep(MINE_RATE / SECONDS)
    mined_block = Block.mine_block(last_block, "bar")

    assert mined_block.difficulty == 1


@pytest.fixture
def last_block() -> Block:
    """
    Fixture for getting a genesis block.

    Returns:
        Block: The genesis block.
    """
    return Block.genesis()


@pytest.fixture
def block(last_block: Block) -> Block:
    """
    Fixture for getting a mined block.

    Args:
        last_block (Block): The block to base the new block on.

    Returns:
        Block: The mined block.
    """
    return Block.mine_block(last_block, "test_data")


def test_is_valid_block(last_block: Block, block: Block) -> None:
    """
    Tests the is_valid_block method of the Block class.

    Args:
        last_block (Block): The block before the block to test.
        block (Block): The block to test.
    """
    Block.is_valid_block(last_block, block)


def test_is_valid_block_bad_last_hash(last_block: Block, block: Block) -> None:
    """
    Tests the is_valid_block method of the Block class with a bad last hash.

    Args:
        last_block (Block): The block before the block to test.
        block (Block): The block to test.
    """
    block.last_hash = "evil_last_hash"

    with pytest.raises(Exception, match="last_hash must be correct"):
        Block.is_valid_block(last_block, block)


def test_is_valid_block_bad_proof_of_work(last_block: Block, block: Block) -> None:
    """
    Tests the is_valid_block method of the Block class with a bad proof of work.

    Args:
        last_block (Block): The block before the block to test.
        block (Block): The block to test.
    """
    block.hash = "fff"

    with pytest.raises(Exception, match="proof of work requirement was not met"):
        Block.is_valid_block(last_block, block)


def test_is_valid_block_jumped_difficulty(last_block: Block, block: Block) -> None:
    """
    Tests the is_valid_block method of the Block class with a jumped difficulty.

    Args:
        last_block (Block): The block before the block to test.
        block (Block): The block to test.
    """
    jumped_difficulty = 10
    block.difficulty = jumped_difficulty
    block.hash = f'{"0" * jumped_difficulty}111abc'

    with pytest.raises(Exception, match="difficulty must only adjust by 1"):
        Block.is_valid_block(last_block, block)


def test_is_valid_block_bad_block_hash(last_block: Block, block: Block) -> None:
    """
    Tests the is_valid_block method of the Block class with a bad block hash.

    Args:
        last_block (Block): The block before the block to test.
        block (Block): The block to test.
    """
    block.hash = "0000000000000000bbbabc"

    with pytest.raises(Exception, match="block hash must be correct"):
        Block.is_valid_block(last_block, block)
