import uuid
import json
from backend.config import STARTING_BALANCE
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
 #The course offers elliptic cryptography.
#We will be using RSA.
#from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric.utils import (
    encode_dss_signature,
    decode_dss_signature
)
from cryptography.hazmat.primitives import hashes,serialization
from cryptography.exceptions import InvalidSignature

class Wallet:
    """
    An individual wallet for the miner.
    This keeps track of the transactions and balance of the wallet.
    The process of utilising the wallet
    1. Facilitate transactions between the peers.
    2. Authorising transactions using digital signatures.
    """
    def __init__(self, blockchain=None):
        self.address = str(uuid.uuid4())[0:8]
        self.private_key = ec.generate_private_key(ec.SECP256K1(), default_backend())
        self.public_key = self.private_key.public_key()
        self.serialize_public_key()
        self.blockchain = blockchain

    @property
    def balance(self):
        return Wallet.calculate_balance(self.blockchain,self.address)

    def sign(self,data):
        """
        Generates the signature using the private key of the user's wallet.
        """
        return decode_dss_signature(self.private_key.sign(
            json.dumps(data).encode('utf-8'), 
            ec.ECDSA(hashes.SHA256())
            )) #Elliptic cryptography digital signature algorithm (ECDSA).

    def serialize_public_key(self):
        """
        Reset the public key to it's serialised version.
        """
        #print(f'\nself.public_key_bytes: {self.public_key_bytes}')
        #print(f'\ndecoded_public_key: {decoded_public_key}')

        self.public_key = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM ,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode('utf-8')

    @staticmethod
    def verify(public_key,data,signature):
        """
        Verifies the data present in the wallet for transaction validation.
        """
        deserialized_public_key = serialization.load_pem_public_key(
            public_key.encode('utf-8'),
            default_backend()
        )

        #print(f'signature: {signature}\n')
        (r,s) = signature #Assigns first value of signature to r and second value of signature to s.

        try:
            deserialized_public_key.verify(
                encode_dss_signature(r,s),
                json.dumps(data).encode('utf-8'),
                ec.ECDSA(hashes.SHA256())
                )
            return True
        except InvalidSignature :
            return False

    @staticmethod
    def calculate_balance(blockchain,address):
        """
        Calculates the balance of the transactions within the given address by considering the recent 
        transaction made in the network.

        The balance is found by adding the output values that belong to the address since the most recent
        transaction made by that address.
        """
        balance = STARTING_BALANCE

        if not blockchain:
            return balance

        for block in blockchain.chain:
            for transaction in block.data:
                if transaction['input']['address'] == address:
                    #Anytime the address conducts a transaction, the balance of the wallet must be reset.
                    balance = transaction['output'][address]
                elif address in transaction['output']:
                    balance += transaction['output'][address]

        return balance

#pk = rsa.generate_private_key(public_exponent=65536,key_size=1024)
#puk = pk.public_key()


def main():
    wallet = Wallet()
    print(f'Wallet.__dict__: {wallet.__dict__}')

    data = {'name':'aditya'}
    signature = wallet.sign(data)
    print(f'signature: {signature}')

    should_be_valid = Wallet.verify(wallet.public_key,data,signature)
    print(f'should be valid : {should_be_valid}')

    should_be_invalid = Wallet.verify(Wallet().public_key,data,signature)
    print(f'should be invalid : {should_be_invalid}')


if __name__ == "__main__":
    main()