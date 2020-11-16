import time

from pubnub.pubnub import PubNub
from pubnub.pnconfiguration import PNConfiguration
from pubnub.callbacks import SubscribeCallback
from backend.blockchain.block import Block
from backend.wallet.transactions import Transactions


"""
This file is required for Publish Subscribe method in the blockchain class which will help in mining data
and help in appending the chain inside the blockchain class.
"""


pnconfig = PNConfiguration()
pnconfig.subscribe_key = 'sub-c-744e489c-168c-11eb-ae19-92aa6521e721'
pnconfig.publish_key = 'pub-c-1efe5c50-88df-4864-9fcc-5258969c4a9c'

CHANNELS = {
    'TEST':'TEST',
    'BLOCK':'BLOCK',
    'TRANSACTION':'TRANSACTION'
}

class Listener(SubscribeCallback):
    def __init__(self,blockchain, transaction_pool):
        self.blockchain = blockchain
        self.transaction_pool = transaction_pool

    def message(self,pubnub, message_object):
        print(f'\n-- Channel: {message_object.channel} | Message: {message_object.message}')
        if message_object.channel == CHANNELS['BLOCK']:
            block = Block.from_json(message_object.message)
            potential_chain = self.blockchain.chain[:]
            potential_chain.append(block)
            try:
                self.blockchain.replace_chain(potential_chain)
                self.transaction_pool.clear_blockchain_transactions(
                    self.blockchain
                )
                print("\n--Successfully replaced the local chain")
            except Exception as e:
                print(f"\n--The chain is not replaced:{e}")

        elif message_object.channel == CHANNELS['TRANSACTION']:
            transaction = Transactions.from_json(message_object.message)
            self.transaction_pool.set_transaction(transaction)
            print('\n-- Set the new transaction in the transaction pool')

            


class PubSub():
    """
    Handles the publish/subscribe layer of the application.
    This also provides communication between the nodes in a blockchain network
    """
    def __init__(self,blockchain, transaction_pool):
        self.pubnub = PubNub(pnconfig)
        self.pubnub.subscribe().channels(CHANNELS.values()).execute() #Pretty long code but this subscribes the channel which
        #later gets executed in the PubNub site.
        self.pubnub.add_listener(Listener(blockchain, transaction_pool))

    def publish(self, channel, message):
        """
        Publish the message object to the channel.
        """
        self.pubnub.publish().channel(channel).message(message).sync()

    def broadcast_block(self,block):
        """
        This will broadcast a block to all of it's nodes.
        """
        self.publish(CHANNELS['BLOCK'],block.to_json())

    def broadcast_transaction(self, transaction):
        """
        Broadcast a transaction to all the nodes.
        """
        self.publish(CHANNELS['TRANSACTION'],transaction.to_json())

def main():
    pubsub = PubSub()
    time.sleep(1)
    pubsub.publish(CHANNELS['TEST'],{'foo':'bar'})
    

if __name__=='__main__':
    main()