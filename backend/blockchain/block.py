import time
from typing import Any, List

from backend.utils.crypto_hash import crypto_hash
from backend.utils.hex_to_binary import hex_to_binary
from backend.config import MINE_RATE

GENESIS_DATA = {
    "timestamp": 1,
    "last_hash": "genesis_last_hash",
    "hash": "genesis_hash",
    "data": [],
    "difficulty": 3,
    "nonce": "genesis_nonce",
}


class Block:
    """
    Block: a unit of storage.
    Store transactions in a blockchain that supports a cryptocurrency.
    """

    def __init__(
        self,
        timestamp: int,
        last_hash: str,
        hash: str,
        data: List[Any],
        difficulty: int,
        nonce: str,
    ):
        """
        Initialize a Block instance.

        Args:
            timestamp (int): Timestamp of creation.
            last_hash (str): Hash of the preceding block.
            hash (str): Hash of this block.
            data (List[Any]): Data stored in the block.
            difficulty (int): Difficulty level for proof-of-work.
            nonce (str): Nonce value.
        """

        self.timestamp = timestamp
        self.last_hash = last_hash
        self.hash = hash
        self.data = data
        self.difficulty = difficulty
        self.nonce = nonce

    def __repr__(self) -> str:
        """
        Return a string representation of the Block.

        Returns:
            str: String representation of the Block.
        """
        return (
            "Block("
            f"timestamp: {self.timestamp}, "
            f"last_hash: {self.last_hash}, "
            f"hash: {self.hash}, "
            f"data: {self.data}, "
            f"difficulty: {self.difficulty}, "
            f"nonce: {self.nonce})"
        )

    def __eq__(self, other: "Block") -> bool:
        """
        Check the equality of two blocks.

        Args:
            other (Block): Another Block instance.

        Returns:
            bool: True if blocks are equal, False otherwise.
        """
        return self.__dict__ == other.__dict__

    def to_json(self) -> dict:
        """
        Serialize the block into a dictionary of its attributes.

        Returns:
            dict: A dictionary containing Block attributes.
        """
        return self.__dict__

    @staticmethod
    def mine_block(last_block: "Block", data: List[Any]) -> "Block":
        """
        Mine a block based on the given last_block and data, until a block hash
        is found that meets the leading 0's proof of work requirement.

        Args:
            last_block (Block): The last Block in the Blockchain.
            data (List[Any]): Data to be included in the Block.

        Returns:
            Block: The newly mined Block.
        """
        timestamp = time.time_ns()
        last_hash = last_block.hash
        difficulty = Block.adjust_difficulty(last_block, timestamp)
        nonce = 0
        hash = crypto_hash(timestamp, last_hash, data, difficulty, nonce)

        while hex_to_binary(hash)[0:difficulty] != "0" * difficulty:
            nonce += 1
            timestamp = time.time_ns()
            difficulty = Block.adjust_difficulty(last_block, timestamp)
            hash = crypto_hash(timestamp, last_hash, data, difficulty, nonce)

        return Block(timestamp, last_hash, hash, data, difficulty, nonce)

    @staticmethod
    def genesis() -> "Block":
        """
        Generate the genesis block.

        Returns:
            Block: The genesis Block.
        """
        return Block(**GENESIS_DATA)

    @staticmethod
    def from_json(block_json: dict) -> "Block":
        """
        Deserialize a block's json representation back into a block instance.

        Args:
            block_json (dict): A JSON representation of a Block.

        Returns:
            Block: A Block instance.
        """
        return Block(**block_json)

    @staticmethod
    def adjust_difficulty(last_block: "Block", new_timestamp: int) -> int:
        """
        Calculate the adjusted difficulty according to the MINE_RATE.
        Increase the difficulty for quickly mined blocks.
        Decrease the difficulty for slowly mined blocks.

        Args:
            last_block (Block): The last Block in the Blockchain.
            new_timestamp (int): The new timestamp.

        Returns:
            int: The adjusted difficulty.
        """
        if (new_timestamp - last_block.timestamp) < MINE_RATE:
            return last_block.difficulty + 1

        if (last_block.difficulty - 1) > 0:
            return last_block.difficulty - 1

        return 1

    @staticmethod
    def is_valid_block(last_block: "Block", block: "Block") -> None:
        """
        Validate block by enforcing the following rules:
          - the block must have the proper last_hash reference
          - the block must meet the proof of work requirement
          - the difficulty must only adjust by 1
          - the block hash must be a valid combination of the block fields

        Args:
            last_block (Block): The last Block in the Blockchain.
            block (Block): The Block to be validated.

        Raises:
            Exception: If any of the validation rules are broken.
        """
        if block.last_hash != last_block.hash:
            raise Exception("The block last_hash must be correct")

        if hex_to_binary(block.hash)[0 : block.difficulty] != "0" * block.difficulty:
            raise Exception("The proof of work requirement was not met")

        if abs(last_block.difficulty - block.difficulty) > 1:
            raise Exception("The block difficulty must only adjust by 1")

        reconstructed_hash = crypto_hash(
            block.timestamp, block.last_hash, block.data, block.nonce, block.difficulty
        )

        if block.hash != reconstructed_hash:
            raise Exception("The block hash must be correct")


def main() -> None:
    """
    Demonstrate the validation of a block in the Blockchain.
    """
    genesis_block = Block.genesis()
    bad_block = Block.mine_block(genesis_block, "foo")
    bad_block.last_hash = "evil_data"

    try:
        Block.is_valid_block(genesis_block, bad_block)
    except Exception as e:
        print(f"is_valid_block: {e}")


if __name__ == "__main__":
    main()
