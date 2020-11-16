import requests
import time
from backend.wallet.wallet import Wallet

BASE_URL = 'http://localhost:5000'

def get_blockchain():
    return requests.get(f'{BASE_URL}/blockchain').json()

def get_blockchain_mine():
    return requests.get(f'{BASE_URL}/blockchain/mine').json()

def  post_wallet_transact(recepient,amount):
    return requests.post(
        f'{BASE_URL}/wallet/transact',
        json={'recepient':recepient, 'amount':amount},
        ).json()

def get_wallet_info():
    return requests.get(f'{BASE_URL}/wallet/info').json()

start_blockchain = get_blockchain()
print(f'start_blockchain : {start_blockchain}')

recepient = Wallet().address

post_wallet_transact_1 = post_wallet_transact(recepient,21)
print(f'\npost_wallet_transact_1 : {post_wallet_transact_1}')

time.sleep(1)
post_wallet_transact_2 = post_wallet_transact(recepient,15)
print(f'\npost_wallet_transact_2 : {post_wallet_transact_2}')

time.sleep(1.00)
mine_block_value = get_blockchain_mine()
print(f'\nmine_block_value : {mine_block_value}')

wallet_info = get_wallet_info()
print(f'\nwallet_info: {wallet_info}')