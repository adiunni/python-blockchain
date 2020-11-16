from backend.wallet.transaction_pool import TransactionPool
from backend.wallet.transactions import Transactions
from backend.wallet.wallet import Wallet
from backend.blockchain.blockchain import Blockchain

def test_set_transactions():
    transaction_pool =TransactionPool()
    test_transaction = Transactions(Wallet(),'recepient',10)
    transaction_pool.set_transaction(test_transaction)

    assert transaction_pool.trasaction_map[test_transaction.id] == test_transaction

def test_clear_blockchain_transactions():
    transaction_pool = TransactionPool()
    transaction1 = Transactions(Wallet(),'recepient',2)
    transaction2 = Transactions(Wallet(),'recepient',1)
    transaction_pool.set_transaction(transaction1)
    transaction_pool.set_transaction(transaction2)

    blockchain = Blockchain()
    blockchain.addBlock([transaction1.to_json(),transaction2.to_json()])
    
    assert transaction1.id in transaction_pool.trasaction_map
    assert transaction2.id in transaction_pool.trasaction_map

    transaction_pool.clear_blockchain_transactions(blockchain)

    assert not transaction1.id in transaction_pool.trasaction_map
    assert not transaction2.id in transaction_pool.trasaction_map