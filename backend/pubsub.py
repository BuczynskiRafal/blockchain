import os
import time

from dotenv import load_dotenv
from pubnub.callbacks import SubscribeCallback
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub

from backend.blockchain.block import Block
from backend.blockchain.blockchain import Blockchain

load_dotenv()

pnconfig = PNConfiguration()
pnconfig.subscribe_key = os.environ.get("subscribe_key")
pnconfig.publish_key = os.environ.get("publish_key")

CHANNELS = {"TEST": "TEST", "BLOCK": "BLOCK", "TRANSACTION": "TRANSACTION"}


class Listener(SubscribeCallback):
    def __init__(self, blockchain, transaction_pool) -> None:
        """
        Listener for handling messages in the channels.

        Args:
            blockchain (Blockchain): The blockchain instance.
            transaction_pool (TransactionPool): The transaction pool instance.
        """
        self.blockchain = blockchain
        self.transaction_pool = transaction_pool

    def message(self, pubnub, message_object) -> None:
        """
        Handle new messages arriving on the channel.

        Args:
            pubnub (PubNub): The PubNub instance.
            message_object (MessageObject): The new message instance.
        """
        print(f"\n-- Channel: {message_object.channel} | Message: {message_object.message}")

        if message_object.channel == CHANNELS["BLOCK"]:
            block = Block.from_json(message_object.message)
            potential_chain = self.blockchain.chain[:]
            potential_chain.append(block)

            try:
                self.blockchain.replace_chain(potential_chain)
                self.transaction_pool.clear_blockchain_transactions(self.blockchain)
                print("\n -- Successfully replaced the local chain")
            except Exception as e:
                print(f"\n -- Did not replace chain: {e}")
        elif message_object.channel == CHANNELS["TRANSACTION"]:
            # self.transaction_pool.set_transaction(transaction)
            print("\n -- Set the new transaction in the transaction pool")


class PubSub:
    """
    Handles the publish/subscribe layer of the application.
    Provides communication between the nodes of the blockchain network.
    """

    def __init__(self, blockchain: Blockchain) -> None:
        self.pubnub = PubNub(pnconfig)
        self.pubnub.subscribe().channels(CHANNELS.values()).execute()

    def publish(self, channel, message):
        """
        Publish the message object to the channel.

        Args:
            channel (str): The name of the channel.
            message (dict): The message to be published.
        """
        self.pubnub.unsubscribe().channels([channel]).execute()
        self.pubnub.publish().channel(channel).message(message).sync()
        self.pubnub.subscribe().channels([channel]).execute()

    def broadcast_block(self, block: Block) -> None:
        """
        Broadcast a block object to all nodes.

        Args:
            block (Block): The block to be broadcast.
        """
        self.publish(CHANNELS["BLOCK"], block.to_json())

    def broadcast_transaction(self, transaction) -> None:
        """
        Broadcast a transaction to all nodes.

        Args:
            transaction (Transaction): The transaction to be broadcast.
        """
        self.publish(CHANNELS["TRANSACTION"], transaction.to_json())


def main() -> None:
    """
    Main function to demonstrate the usage of the PubSub class.
    """
    pubsub = PubSub()

    time.sleep(1)

    pubsub.publish(CHANNELS["TEST"], {"foo": "bar"})


if __name__ == "__main__":
    main()
