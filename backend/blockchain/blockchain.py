"""Module containg Blockchain class."""
from backend.blockchain.block import Block


class Blockchain:
    """
    Blockchain is a public ledger of transactions.
    Implement as a list of blocks - data sets of transactions.
    """

    def __init__(self):
        self.chain = [Block.genesis()]

    def __repr__(self):
        return f"Blockchain: {str(self.chain)}"

    def add_block(self, data):
        self.chain.append(Block.mine_block(self.chain[-1], data))


def main():
    blockchain = Blockchain()
    blockchain.add_block("first")
    blockchain.add_block("second")

    print(blockchain)


if __name__ == "__main__":
    main()
