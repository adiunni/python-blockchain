from backend.blockchain.block import Block
from backend.wallet.transactions import Transactions
from backend.wallet.wallet import Wallet
from backend.config import MINING_REWARD_INPUT

class Blockchain:
    """
    Blockchain: Distributed public ledger. Used to store the data and it is a decentralised environment.
    This contains the block class which is linked with each other via a chain hence known as blockchain.
    """
    def __init__(self):
         self.chain = [Block.genesis()] #Stores all the blocks in a list.

    def addBlock(self,data):
        """
        Adds the block into the chain by using list methods.
        """
        self.chain.append(Block.mine_block(self.chain[-1],data))

    def __repr__(self): # Class used to print out the blockchain method (Required in block class as well).
        #Without the __repr__ method, the print statement will print the memory address of the class.
        return f'Blockchain: \n {self.chain}'

    def replace_chain(self,chain):
        """
        Replace the local chain if the following rules apply.
        1. The incoming chain must be longer than the local one
        2. The incoming chain should be formatted properly.
        """
        if len(chain) <= len(self.chain):
            raise Exception('Cannot replace. The chain must be longer')

        try:
            Blockchain.ischainvalid(chain)
        except Exception as e:
            raise Exception(f'Cannot replace. The incoming chain is invalid: {e}')

        self.chain = chain

    def to_json(self):
        """
        Serialize the blockchain into a list of blocks. This function tries to convert the object into
        JSON format.
        """
        return list(map(lambda block: block.to_json(),self.chain))

    @staticmethod
    def from_json(chain_json):
        """
        Deserialize a list of chain blocks back to it's blockchain instance.
        The result will contain the chain list of Block instances.
        """
        blockchain = Blockchain()
        blockchain.chain = list(map(lambda block_json: Block.from_json(block_json),chain_json))
        return blockchain

    @staticmethod
    def ischainvalid(chain):
        """
        This will validate the incoming chain.
        This should enforce the following conditions
        1. The chain must start with the genesis block
        2. The blocks must be formatted correctly
        """

        if chain[0]!= Block.genesis(): #Exception is raised when the genesis block 
            #is invalid
            raise Exception('The genesis block must be valid')

        for i in range(1,len(chain)):
            block = chain[i]
            last_block = chain[i-1]
            Block.isblockvalid(last_block,block) #It basically checks the validity of
            #each block

        Blockchain.is_valid_transaction_chain(chain)

    @staticmethod
    def is_valid_transaction_chain(chain):
        """
        Enforce the rules of a chain composed of the blocks of transaction
        1. Each transaction must appear in the chain only once.
        2. There must be only one reward per transaction.
        3. Each transaction must be valid.
        """
        transaction_ids = set()
        for i in range(len(chain)):
            block = chain[i]
            has_mining_reward = False

            for transaction_json in block.data:
                transaction = Transactions.from_json(transaction_json)

                if transaction.id in transaction_ids:
                    raise Exception(f'Transaction:{transaction.id} is not unique')

                transaction_ids.add(transaction.id)

                if transaction.input == MINING_REWARD_INPUT:
                    if has_mining_reward:
                        raise Exception(
                                'There can only be one mining reward per block.'\
                                f'Check block with hash {block.hash}'
                            )
                    has_mining_reward = True
                else:
                    historic_blockchain = Blockchain()
                    historic_blockchain.chain = chain[0:i]
                    historic_balance = Wallet.calculate_balance(
                        historic_blockchain,
                        transaction.input['address']
                    )
                    if historic_balance != transaction.input['amount']:
                        raise Exception(f'Transaction {transaction.id} has an invalid amount')

                Transactions.is_valid_transaction(transaction)

def main(): # Wrap the function around the 
    blockchain = Blockchain()
    blockchain.addBlock('one')
    blockchain.addBlock('two')
    blockchain.addBlock('three')
    blockchain.addBlock('four')

    print(blockchain)
    #print(f'blockchain.py __name__: {__name__}')

if __name__ == '__main__':
    main()
