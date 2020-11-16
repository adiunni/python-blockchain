from backend.blockchain.blockchain import Blockchain
from backend.blockchain.block import GENESIS_DATA
from backend.wallet.wallet import Wallet
from backend.wallet.transactions import Transactions
import pytest

def test_blockchain_instance():
     """
     Tests if the blockchain has the start as genesis data
     """
     blockchain = Blockchain()

     assert blockchain.chain[0].hash == GENESIS_DATA['hash']

def test_addBlock():
     """
     Tests if the add block function works as intended.
     """
     blockchain = Blockchain()
     data = 'test-data'
     blockchain.addBlock(data)
     assert blockchain.chain[-1].data == data

@pytest.fixture #this is similar to a global variable declaration 
def three_blocks_chain():
     blockhain = Blockchain()
     for i in range(3):
          blockhain.addBlock([Transactions(Wallet(),'recepient',i).to_json()])
     return blockhain

def test_is_valid_chain(three_blocks_chain):
     """
     Checks if the chain is valid or not
     """
     Blockchain.ischainvalid(three_blocks_chain.chain)

def test_valid_chain_with_bad_genesis(three_blocks_chain):
     """
     This checks if there is any bad genesis block which will prevent tampering of first genesis block.
     """
     three_blocks_chain.chain[0].hash = 'bad_hash'
     with pytest.raises(Exception, match='The genesis block must be valid'):
          Blockchain.ischainvalid(three_blocks_chain.chain)

@pytest.fixture #Another global variable kind of declaration
def blockchain():
     return Blockchain()

def test_replace_chain(three_blocks_chain,blockchain): 
     """
     Checks if the incoming chain is longer than the existing chain.
     If so then the chain is replaced otherwise the existing chain is continued
     """
     blockchain.replace_chain(three_blocks_chain.chain)

     assert blockchain.chain == three_blocks_chain.chain

def test_replace_chain_not_longer(three_blocks_chain,blockchain):
     """
     Checks for the case if the incoming chain is not longer than the existing chain.
     """
     with pytest.raises(Exception,match='Cannot replace. The chain must be longer'):
          three_blocks_chain.replace_chain(blockchain.chain)

def test_replace_chain_bad_chain(three_blocks_chain,blockchain):
     """
     Checks for the case that if the incoming chain has an invalid data.
     """
     three_blocks_chain.chain[1].hash ='bad_hash'
     with pytest.raises(Exception,match='The incoming chain is invalid'):
          blockchain.replace_chain(three_blocks_chain.chain)

def test_valid_transaction_chain(three_blocks_chain):
     Blockchain.is_valid_transaction_chain(three_blocks_chain.chain)

def test_is_valid_transaction_chain_duplicate_transaction(three_blocks_chain):
     transaction = Transactions(Wallet(),'recepient',1).to_json()
     three_blocks_chain.addBlock([transaction,transaction])
     with pytest.raises(Exception,match='is not unique'):
          Blockchain.is_valid_transaction_chain(three_blocks_chain.chain)

def test_is_valid_transaction_chain_multiple_rewards(three_blocks_chain):
     reward_1 = Transactions.reward_transaction(Wallet()).to_json()
     reward_2 = Transactions.reward_transaction(Wallet()).to_json()
     three_blocks_chain.addBlock([reward_1,reward_2])
     with pytest.raises(Exception,match='one mining reward per block'):
          Blockchain.is_valid_transaction_chain(three_blocks_chain.chain)

def test_is_valid_transaction_chain_bad_transaction(three_blocks_chain):
     bad_transaction = Transactions(Wallet(),'recepient',1)
     bad_transaction.input['signature'] = Wallet().sign(bad_transaction.output)
     three_blocks_chain.addBlock([bad_transaction.to_json()])
     with pytest.raises(Exception):
          Blockchain.is_valid_transaction_chain(three_blocks_chain.chain)

def test_is_valid_transaction_chain_bad_historic_balance(three_blocks_chain):
     wallet = Wallet()
     bad_transaction = Transactions(wallet,'recepient',10)
     bad_transaction.output[wallet.address] = 10000
     bad_transaction.input['amount'] = 10010
     bad_transaction.input['signature'] = wallet.sign(bad_transaction.output)
     three_blocks_chain.addBlock([bad_transaction.to_json()])

     with pytest.raises(Exception,match='has an invalid amount'):
          Blockchain.is_valid_transaction_chain(three_blocks_chain.chain)








