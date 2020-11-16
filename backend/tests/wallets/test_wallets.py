from backend.wallet.wallet import Wallet 
from backend.blockchain.blockchain import Blockchain
from backend.wallet.transactions import Transactions
from backend.config import STARTING_BALANCE

def test_verify_validsignature():
    data = {'name':'aditya'}
    wallet = Wallet()
    signature = wallet.sign(data)

    assert Wallet.verify(wallet.public_key,data,signature)


def test_verify_invalid_signature():
    data = {'name':'aditya'}
    wallet = Wallet()
    signature = wallet.sign(data)
    assert not Wallet.verify(Wallet().public_key,data,signature)

def test_calculate_balance():
    blockchain = Blockchain()
    wallet = Wallet()

    assert Wallet.calculate_balance(blockchain,wallet.address) == STARTING_BALANCE

    amount = 50
    transaction = Transactions(wallet,'recepient',amount)
    blockchain.addBlock([transaction.to_json()])

    assert Wallet.calculate_balance(blockchain,wallet.address) == STARTING_BALANCE - amount

    recvd_amount_1 = 100
    recvd_transaction_1 = Transactions(
        Wallet(),
        wallet.address,
        recvd_amount_1
    )

    recvd_amount_2 = 90
    recvd_transaction_2 = Transactions(
        Wallet(),
        wallet.address,
        recvd_amount_2
    )

    blockchain.addBlock([recvd_transaction_1.to_json(),recvd_transaction_2.to_json()])

    assert Wallet.calculate_balance(blockchain,wallet.address) == \
        STARTING_BALANCE - amount + recvd_amount_1 + recvd_amount_2



    