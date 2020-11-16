from backend.wallet.transactions import Transactions
from backend.wallet.wallet import Wallet
from backend.config import MINING_REWARD, MINING_REWARD_INPUT
import pytest

def test_transaction():
    sender_wallet = Wallet()
    recepient = 'recepient'
    amount = 100
    transaction = Transactions(sender_wallet,recepient,amount)

    assert transaction.output[recepient] == amount
    assert transaction.output[sender_wallet.address] == sender_wallet.balance - amount
    assert 'timestamp' in transaction.input
    assert transaction.input['amount'] == sender_wallet.balance
    assert transaction.input['address'] == sender_wallet.address
    assert transaction.input['public_key'] == sender_wallet.public_key

    assert Wallet.verify(
        transaction.input['public_key'],
        transaction.output,
        transaction.input['signature']
    )

def test_transaction_exceeds_balance():
    with pytest.raises(Exception, match="Amount exceeds the balance"):
        Transactions(Wallet(),'recepient',9001)

def test_transaction_update_exceeds_balance():
    sender_wallet = Wallet()
    transaction = Transactions(sender_wallet,'recepient',100)
    with pytest.raises(Exception, match="Amount exceeds the balance"):
        transaction.update(sender_wallet,'new_recepient',9001)

def test_transaction_update():
    sender_wallet = Wallet()
    first_recepient = 'first_recepient'
    first_amount = 50
    transaction = Transactions(sender_wallet,first_recepient,first_amount)

    next_recepient = 'next_recepient'
    next_amount = 75
    transaction.update(sender_wallet,next_recepient,next_amount)

    assert transaction.output[next_recepient] == next_amount
    assert transaction.output[sender_wallet.address] == sender_wallet.balance - first_amount - next_amount
    assert Wallet.verify(
        transaction.input['public_key'],
        transaction.output,
        transaction.input['signature']
    )

    to_first_again_amount = 25
    transaction.update(sender_wallet,first_recepient,to_first_again_amount)

    assert transaction.output[first_recepient] == first_amount + to_first_again_amount
    assert transaction.output[sender_wallet.address] == sender_wallet.balance - first_amount - next_amount \
        - to_first_again_amount
    assert Wallet.verify(
        transaction.input['public_key'],
        transaction.output,
        transaction.input['signature']
    )
    
def test_valid_transaction():
    Transactions.is_valid_transaction(Transactions(Wallet(),'recepient',50))

def test_valid_transaction_with_invalid_outputs():
    sender_wallet = Wallet()
    transaction = Transactions(sender_wallet,'recepient',50)
    transaction.output[sender_wallet.address]= 9001
    with pytest.raises(Exception, match="Invalid transaction output values."):
        Transactions.is_valid_transaction(transaction)

def test_valid_transaction_with_invalid_signature():
    transaction = Transactions(Wallet(),'recepient',50)
    transaction.input['signature'] = Wallet().sign(transaction.output)
    with pytest.raises(Exception,match='Invalid signature'):
        Transactions.is_valid_transaction(transaction)

def test_reward_miner():
    miner_wallet = Wallet()
    transaction = Transactions.reward_transaction(miner_wallet)

    assert transaction.input == MINING_REWARD_INPUT
    assert transaction.output[miner_wallet.address] == MINING_REWARD

def test_valid_reward_transactions():
    reward_transaction = Transactions.reward_transaction(Wallet())
    Transactions.is_valid_transaction(reward_transaction)

def test_invalid_reward_transaction_extra_recepient():
    reward_transaction = Transactions.reward_transaction(Wallet())
    reward_transaction.output['extra_recepient'] = 60

    with pytest.raises(Exception,match='Invalid mining reward'):
        Transactions.is_valid_transaction(reward_transaction)

def test_invalid_reward_transaction_invalid_amount():
    miner_wallet = Wallet()
    reward_transaction = Transactions.reward_transaction(Wallet())
    reward_transaction.output[miner_wallet.address] = 912091

    with pytest.raises(Exception,match='Invalid mining reward'):
        Transactions.is_valid_transaction(reward_transaction)





