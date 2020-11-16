import time
from backend.util.crypto_hash import crypto_hash
from backend.util.hex_to_bin import hex_to_bin
from backend.config import MINE_RATE

GENESIS_DATA = {
    'number' : 0,
    'timestamp' : 1,
    'timerec' : '0',
    'last_hash' : 'genesis_last_hash',
    'hash' : 'genesis_hash',
    'data' : [],
    'difficulty': 3,
    'nonce':'genesis_nonce'
}

class Block:
    """
    Block is a fundamental part of the Blockchain. This is because it stores all the data present in a 
    transaction or anything else related to storing of data.
    The block contains the following data.
    1. Number: The block number in the chain
    2. Timestamp: Recorded in nanoseconds.
    3. Time recorded: This is given so that it outputs the time in Days Months year and seconds format
    4. Hash: A unique hexadecimal number which defines the authencity of that block.
    5. Last hash: It is the hash value of the previous block.
    6. Data: The actual data inside the block.
    7. Difficulty: The number of leading zero's in the hash (binary value).
    8. Nonce: The number of iterations took to match the hash with the proper number of leading zeros.
    """
    def __init__(self,number,timestamp,timerec,last_hash, hash, data, difficulty, nonce):
        self.number = number
        self.timestamp = timestamp
        self.timerec = timerec
        self.hash = hash
        self.last_hash = last_hash
        self.data = data
        self.difficulty= difficulty # Number of leading zeros in the block hash.
        self.nonce= nonce # Number of iterations required to reach the valid hash.

    def __repr__(self): #This method is required to print out the class value of the block.
        return(
            f'Block-number: {self.number}\n'
            f'Block-time recorded: {self.timerec}\n' #Prints the date and time of the block entry.
            f'Block-timestamp: {self.timestamp}\n'
            f'Block-hash: {self.hash}\n'
            f'Block-last_hash: {self.last_hash}\n'
            f'Block-data: {self.data}\n'
            f'Difficulty: {self.difficulty}\n'
            f'Nonce: {self.nonce}\n\n'
        )

    def __eq__(self,other): #It is another hidden class which will equate the 
        #given instances in the form of a dictionary.
        return self.__dict__ == other.__dict__

    def to_json(self):
        """
        This serializes the block into it's dictionary representation. This is readable in JSON.
        """
        return self.__dict__

    @staticmethod
    def mine_block(last_block, data):
        """
        Mining is a process which is used to add block into the chain through use of computational
        power. This process can become expensive as well as this can become easy to implement.
        We will keep on producing more data until we reach the leading 0's requirement for proof of work
        """
        number = last_block.number + 1
        timestamp = time.time_ns() # Returns time in nanoseconds .
        last_hash = last_block.hash
        difficulty = Block.adjust_diff(last_block,timestamp)
        nonce = 0
        hash = crypto_hash(timestamp, last_hash, data, difficulty, nonce)

        while hex_to_bin(hash)[0:difficulty] != '0' * difficulty: # We need to add leading zeroes according to difficulty
            #This process converts the code into binary format of hexadecimal hash value and then enters the loop
            nonce += 1 #Nonce value is incremented to one everytime this loop is executed
            timestamp = time.time_ns() #This is necessary.
            difficulty = Block.adjust_diff(last_block,timestamp) #Difficulty will get itself adjusted according to current block timestamp.
            hash = crypto_hash(timestamp, last_hash, data, difficulty, nonce)    
        
        timerec = time.asctime() # Returns time in form of string.

        return Block(number,timestamp,timerec,last_hash, hash, data, difficulty, nonce)

    @staticmethod
    def genesis():
        """
        Generates the genesis block. Genesis block is the first block in the blockchain.
        """
        return Block(**GENESIS_DATA) #Double asterisks are used to unpack the data
        #present in the GENESIS_DATA dictionary. This is one convenient method.

    @staticmethod
    def from_json(block_json):
        """
        To deserialize a block from it's JSON format back to a block instance
        """
        return Block(**block_json) 

    @staticmethod
    def adjust_diff(last_block,new_timestamp):
        """
        Calculate the difficulty with respect to MINE_RATE.
        If the difficulty is high we will decrement it by 1.(Slowly mined blocks)
        Else we will increment it by 1 (Quickly mined blocks)
        """
        if(new_timestamp - last_block.timestamp) < MINE_RATE :
            return last_block.difficulty + 1
        if(last_block.difficulty-1)>0:
            return last_block.difficulty - 1

        return 1

    @staticmethod
    def isblockvalid(last_block,block):
        """
        Validates the block using the following conditions
        1. Is block.last_hash == last_block.hash
        2. The block must meet the proof of work requirement.
        3. The difficulty must only be changed by 1.
        4. The block hash must be a valid combination of all the required fields.
        """

        if block.last_hash != last_block.hash:
            raise Exception("The block hash is invalid")

        if hex_to_bin(block.hash)[0:block.difficulty] != '0'*block.difficulty :
            raise Exception('The PoW requirement was not met')
        
        if abs(last_block.difficulty - block.difficulty) > 1:
            raise Exception('The difficulty level must only adjusted by one')

        reconst_hash = crypto_hash(
            block.timestamp,
            block.last_hash,
            block.data,
            block.difficulty,
            block.nonce
        )

        if block.hash != reconst_hash:
            raise Exception('The block hash must be correct')



def main():
    gen_block = Block.genesis()
    good_block = Block.mine_block(gen_block,'Hello')
    #bad_block.last_hash = 'Fished the hash'
    try:
        Block.isblockvalid(gen_block,good_block)
    
    except Exception as e:
        print(f'isblockvalid:{e}')


if __name__ == '__main__':
    main()