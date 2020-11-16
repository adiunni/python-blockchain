import uuid
import time

from backend.wallet.wallet import Wallet
from backend.config import MINING_REWARD, MINING_REWARD_INPUT
class Transactions:
    """
    This will document an exchange of currency from one or more accounts to 
    one or another.
    """
    def __init__(
            self,
            sender_wallet = None,
            recepient = None,
            amount=None,
            id = None,
            input = None,
            output = None
        ):
        self.id = id or str(uuid.uuid4())[0:8]
        self.output = output or self.create_output(
            sender_wallet,
            recepient,
            amount
        )

        self.input = input or self.create_input(
            sender_wallet,
            self.output
        ) 
    
    def create_output(self,sender_wallet,recepient,amount):
        """
        Structure the output data for the transactions. 
        """
        if amount > sender_wallet.balance :
            raise Exception('Amount exceeds the balance.')

        output = {}
        output[recepient] = amount
        output[sender_wallet.address] = sender_wallet.balance - amount

        return output

    def create_input(self,sender_wallet,output):
        """
        Structure the output data for the transactions.
        Also signs and verify the data of the transactions using the public key and address. 
        """

        return {
            'timestamp' : time.time_ns(),
            'timerec':time.asctime(),
            'amount':sender_wallet.balance,
            'address':sender_wallet.address,
            'public_key':sender_wallet.public_key,
            'signature':sender_wallet.sign(output)
        }

    def update(self, sender_wallet,recepient,amount):
        """
        Update the transactions with an existing or new receipient.
        """
        if amount > self.output[sender_wallet.address]:
            raise Exception("Amount exceeds the balance")

        if recepient in self.output:
            self.output[recepient] = self.output[recepient] + amount
        else:
            self.output[recepient] = amount

        self.output[sender_wallet.address] = self.output[sender_wallet.address] - amount

        self.input = self.create_input(sender_wallet,self.output)

    def to_json(self):
        """
        Serialise the data into it's JSON format.
        """
        return self.__dict__

    @staticmethod
    def from_json(transaction_json):
        """
        Deserialize the JSON format back to Transaction instance
        """
        return Transactions(
            **transaction_json
        )

    @staticmethod
    def is_valid_transaction(transaction):
        """
        Validate the transactions and raises exception for invalid transactions.
        """
        if transaction.input == MINING_REWARD_INPUT:
            if list(transaction.output.values()) != [MINING_REWARD]:
                raise Exception('Invalid mining reward')
            return


        output_total = sum(transaction.output.values())

        if transaction.input['amount'] != output_total:
            raise Exception("Invalid transaction output values.")
    
        if not Wallet.verify(
            transaction.input['public_key'],
            transaction.output,
            transaction.input['signature']
        ):
            raise Exception("Invalid signature")

    @staticmethod
    def reward_transaction(miner_wallet):
        """
        Generates a reward transaction for the miner.
        """
        output = {}
        output[miner_wallet.address] = MINING_REWARD

        return Transactions(input=MINING_REWARD_INPUT,output=output)


def main():
    transaction = Transactions(Wallet(),'Recepient',20)
    print(f'Transaction.__dict__ : {transaction.__dict__}')
    transaction_json = transaction.to_json()
    restored_transaction_json = Transactions.from_json(transaction_json)

    print(f"\nrestored_transaction.__dict__: {restored_transaction_json.__dict__}\n")


if __name__ == "__main__":
    main()

