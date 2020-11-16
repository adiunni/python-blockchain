import os
import requests #Sends GET and POST requests in the application
import random

from flask import Flask , jsonify, request #This imports the Flask and jsonify class from the flask module.

from backend.blockchain.blockchain import Blockchain #Required to GET the blockchain data.
from backend.wallet.wallet import Wallet
from backend.wallet.transactions import Transactions
from backend.wallet.transaction_pool import TransactionPool
from backend.pubsub import PubSub

app = Flask(__name__) #Flask class takes one parameter which is name.
#This creates a class for endpoints. e.g. www.google.com/drive/
#Here /drive is an endpoint to access google drive.
blockchain = Blockchain()
wallet = Wallet(blockchain)
transaction_pool = TransactionPool()
pubsub = PubSub(blockchain,transaction_pool)

#for i in range(3):
    #blockchain.addBlock(i)

@app.route('/') #This will output the default page of the website.
def route_default():
    return 'Welcome to the blockchian'

@app.route('/blockchain')#This will output the blockchain as a class.
def route_blockchain():
    return jsonify(blockchain.to_json())

@app.route('/blockchain/mine')#This will output the method to mine data inside the blockchain class.
def route_blockchain_mine():
    transaction_data = transaction_pool.transaction_data()
    transaction_data.append(Transactions.reward_transaction(wallet).to_json())
    blockchain.addBlock(transaction_data)
    block = blockchain.chain[-1]
    pubsub.broadcast_block(block)
    transaction_pool.clear_blockchain_transactions(blockchain)

    return jsonify(block.to_json())

@app.route('/wallet/transact',methods=['POST'])
def route_wallet_transact():
    transaction_data = request.get_json()
    transaction = transaction_pool.existing_transaction(wallet.address)

    if transaction:
        transaction.update(
            wallet,
            transaction_data['recepient'],
            transaction_data['amount']
            )
    else:
        transaction = Transactions(
            wallet,
            transaction_data['recepient'],
            transaction_data['amount']
        )

    pubsub.broadcast_transaction(transaction)

    return jsonify(transaction.to_json())

@app.route('/wallet/info')
def route_wallet_info():
    return jsonify({'address':wallet.address, 'balance': wallet.balance })


ROOT_PORT = 5000
PORT = ROOT_PORT

if os.environ.get('PEER') == 'True':
    PORT = random.randint(5001,6000)
    result = requests.get(f"http://localhost:{ROOT_PORT}/blockchain")
    result_blockchain = Blockchain.from_json(result.json())
    try:
        blockchain.replace_chain(result_blockchain.chain)
        print("\n --Successfully synchronised the local chain")
    except Exception as e:
        print(f"\n--Error in synchronising: {e}")

    


app.run(port=PORT)