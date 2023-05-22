from typing import List, Any
from backend.blockchain.block import Block


class Blockchain:
    """
    Blockchain: a public ledger of transactions.
    Implemented as a list of blocks - data sets of transactions
    """

    def __init__(self) -> None:
        self.chain = [Block.genesis()]

    def add_block(self, data: Any) -> None:
        """
        Add a new block to the blockchain.

        Args:
            data (Any): Data to be included in the block.
        """
        self.chain.append(Block.mine_block(self.chain[-1], data))

    def __repr__(self) -> str:
        """
        Return a string representation of the Blockchain.

        Returns:
            str: String representation of the Blockchain.
        """
        return f"Blockchain: {self.chain}"

    def replace_chain(self, chain: List[Block]) -> None:
        """
        Replace the local chain with the incoming one if the following applies:
          - The incoming chain is longer than the local one.
          - The incoming chain is formatted properly.

        Args:
            chain (List[Block]): The incoming Blockchain to replace the existing one.

        Raises:
            Exception: If the incoming chain is not longer or is invalid.
        """
        if len(chain) <= len(self.chain):
            raise Exception("Cannot replace. The incoming chain must be longer.")

        try:
            Blockchain.is_valid_chain(chain)
        except Exception as e:
            raise Exception(f"Cannot replace. The incoming chain is invalid: {e}")

        self.chain = chain

    def to_json(self) -> List[dict]:
        """
        Serialize the blockchain into a list of blocks.

        Returns:
            List[dict]: A list of serialized blocks.
        """
        return list(map(lambda block: block.to_json(), self.chain))

    @staticmethod
    def from_json(chain_json: List[dict]) -> "Blockchain":
        """
        Deserialize a list of serialized blocks into a Blockchain instance.
        The result will contain a chain list of Block instances.

        Args:
            chain_json (List[dict]): A JSON representation of a Blockchain.

        Returns:
            Blockchain: A Blockchain instance.
        """
        blockchain = Blockchain()
        blockchain.chain = list(map(lambda block_json: Block.from_json(block_json), chain_json))

        return blockchain

    @staticmethod
    def is_valid_chain(chain: List[Block]) -> None:
        """
        Validate the incoming chain.
        Enforce the following rules of the blockchain:
          - the chain must start with the genesis block
          - blocks must be formatted correctly

        Args:
            chain (List[Block]): The Blockchain to validate.

        Raises:
            Exception: If the genesis block is not valid or blocks are not formatted correctly.
        """
        if chain[0] != Block.genesis():
            raise Exception("The genesis block must be valid")

        for i in range(1, len(chain)):
            block = chain[i]
            last_block = chain[i - 1]
            Block.is_valid_block(last_block, block)

        # Blockchain.is_valid_transaction_chain(chain)

    # @staticmethod
    # def is_valid_transaction_chain(chain: List[Block]) -> None:
    #     """
    #     Enforce the rules of a chain composed of blocks of transactions.
    #         - Each transaction must only appear once in the chain.
    #         - There can only be one mining reward per block.
    #         - Each transaction must be valid.

    #     Args:
    #         chain (List[Block]): The Blockchain to validate.

    #     Raises:
    #         Exception: If there# My response was cut off. I'll complete it now.
    #         are duplicate transactions, more than one mining reward per block, or invalid transactions.
    #     """
    #     transaction_ids = set()

    #     for i in range(len(chain)):
    #         block = chain[i]
    #         has_mining_reward = False

    #         for transaction_json in block.data:
    #             transaction = Transaction.from_json(transaction_json)

    #             if transaction.id in transaction_ids:
    #                 raise Exception(f"Transaction {transaction.id} is not unique")

    #             transaction_ids.add(transaction.id)

    #             if transaction.input == MINING_REWARD_INPUT:
    #                 if has_mining_reward:
    #                     raise Exception(
    #                         "There can only be one mining reward per block. "
    #                         f"Check block with hash: {block.hash}"
    #                     )

    #                 has_mining_reward = True
    #             else:
    #                 historic_blockchain = Blockchain()
    #                 historic_blockchain.chain = chain[0:i]
    #                 historic_balance = Wallet.calculate_balance(
    #                     historic_blockchain, transaction.input["address"]
    #                 )

    #                 if historic_balance != transaction.input["amount"]:
    #                     raise Exception(
    #                         f"Transaction {transaction.id} has an invalid " "input amount"
    #                     )

    #             Transaction.is_valid_transaction(transaction)


def main() -> None:
    """
    Demonstrate adding blocks to a blockchain and printing the blockchain.
    """
    blockchain = Blockchain()
    blockchain.add_block("one")
    blockchain.add_block("two")

    print(blockchain)
    print(f"blockchain.py ___name__: {__name__}")


if __name__ == "__main__":
    main()
