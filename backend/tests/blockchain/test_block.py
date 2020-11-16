import pytest
import time

from backend.blockchain.block import Block,GENESIS_DATA
from backend.config import MINE_RATE,SECONDS
from backend.util.hex_to_bin import hex_to_bin

def test_block():
    """
    This tests the following cases of blockchain
    1.Is it a subclass of Block.
    2.Is the data of the block equal to the given block
    3.Is the  last hash of the block equal to the last block's hash.
    4.Is the block hash leading zero's is equal to the block's difficulty.
    """
    last_block = Block.genesis()
    data = 'test-data'
    block = Block.mine_block(last_block,data)

    assert isinstance(block,Block) 
    assert block.data == data
    assert block.last_hash == last_block.hash
    assert hex_to_bin(block.hash)[0:block.difficulty] == '0' *  block.difficulty

def test_genesis():
    """
    Checks the test cases of the genesis block as 
    1. If it is a subclass of the block 
    2. If the value of the keys and the value in the genesis block is equal.
    """
    genesis = Block.genesis()
    assert isinstance(genesis,Block)
    for key,value in GENESIS_DATA.items():
        getattr(genesis,key) == value

def test_quickly_mined():
    """
    This creates a test case which ensures the increment of difficulty. This occurs when the block is 
    mined in a rate less than the MINE_RATE
    """
    last_block = Block.mine_block(Block.genesis(),"Aditya")
    mined_block = Block.mine_block(last_block,"Unni")

    assert mined_block.difficulty == last_block.difficulty + 1

def test_slow_mined():
    """
    This creates a test case which ensures the decrement of difficulty. This occurs when the block is 
    mined at a rate greater than the MINE_RATE
    """
    last_block = Block.mine_block(Block.genesis(),"Aditya")
    time.sleep(MINE_RATE/SECONDS)
    mined_block = Block.mine_block(last_block,"Unni")

    assert mined_block.difficulty == last_block.difficulty - 1

def test_not_under_1():
    """
    Checks the case that the difficulty doesn't go below 1. This is a necessary test as this will cause
    a worst case scenario when creating a hash of the data.
    """
    last_block = Block(
        1,
        time.time_ns(),
        time.asctime(),
        'last_hash',
        'hash',
        'data',
        1,
        0 
    )
    time.sleep(MINE_RATE/SECONDS)
    mined_block = Block.mine_block(last_block,'hello')

    assert mined_block.difficulty == 1

@pytest.fixture
def last_block():
    return Block.genesis()

@pytest.fixture
def block(last_block):
    return Block.mine_block(last_block,"Adi")

def test_is_valid_block(last_block,block):
    """
    This test focuses on validating a block in the chain which checks the four cases.
    1. Is the last_hash of current block equal to hash of last_block
    2. Does the block meet the proof of work requirements
    3. The difficulty value must be changed by one.
    4. The block hash must contain the hashing of the required fields.
    """
    Block.isblockvalid(last_block,block)

def test_is_valid_block_with_last_hash_bad(last_block,block):
    """
    This test focuses on raising an exception whenever the block hash changes.
    Here we have imported the Pytest module just for this cause, because raising an exception
    should not cause any problems( which usually does ).
    """
    block.last_hash = 'I_m_a_bad_hash'

    with pytest.raises(Exception, match='The block hash is invalid'):
        Block.isblockvalid(last_block,block)

def test_bad_pow(last_block,block):
    """
    This test raises another exception where the Proof of Work is invalid. Here similar code is followed
    like the bad_last_hash_value test. The test will pass if the proper exception is raised.
    """
    block.hash ='fff'
    with pytest.raises(Exception, match='The PoW requirement was not met'):
        Block.isblockvalid(last_block,block)

def test_is_valid_block_jumped_difficulty(last_block,block):
    jumped_difficulty = 10
    block.difficulty = jumped_difficulty
    block.hash = f'{"0"*jumped_difficulty}111abc'
    with pytest.raises(Exception, match='The difficulty level must only adjusted by one'):
        Block.isblockvalid(last_block,block)

def test_is_valid_block_bad_last_hash(last_block,block):
    block.hash = '00000000000000000000000aabbcc'

    with pytest.raises(Exception, match='The block hash must be correct'):
        Block.isblockvalid(last_block,block)