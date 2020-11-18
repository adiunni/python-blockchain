"""
Configuration file to detemine the mining rate hence we can adjust the difficulty 
of the given block being entered in the chain.
Due to time.time_ns(), the output will be in Nanoseconds. To control the mining rate,
we have converted it into seconds hence this config.py file.
"""

NANOSECONDS = 1 
MICROSECONDS = 1000 * NANOSECONDS
MILLISECONDS = 1000 * MICROSECONDS
SECONDS = 1000 * MILLISECONDS

MINE_RATE = 4 * SECONDS

STARTING_BALANCE = 1000

MINING_REWARD = 100
MINING_REWARD_INPUT = {'address':'*--official_mining_reward--*'}