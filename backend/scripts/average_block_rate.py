"""
This is a creation of a script which checks the average block adding rate in the chain.
Now the average rate will be close to the half the value of the MINE_RATE. This is because we
are converting the hash to it's required one in it's hexadecimal form which is easier for CPU
hence we will be converting the following hex value to binary.

"""


from backend.blockchain.blockchain import Blockchain
from backend.config import SECONDS
import time

blockchain = Blockchain()

times = []

for i in range(1000):
    start_time = time.time_ns()
    blockchain.addBlock(i)
    end_time = time.time_ns()

    mining_time = (end_time - start_time) / SECONDS
    times.append(mining_time)

    average_mine_time = sum(times)/ len(times)

    print(f'New block difficulty: {blockchain.chain[-1].difficulty}')
    print(f'Time to mine the block: {mining_time}s')
    print(f'Average time to add blocks: {average_mine_time}s\n')