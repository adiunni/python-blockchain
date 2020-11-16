from backend.util.crypto_hash import crypto_hash

def test_crypto_hash():
    #It should create the same hash for the same data in any order.
    assert crypto_hash(1,[2],'three',) == crypto_hash('three',[2],1)
    assert crypto_hash('aditya') == '0a60ced43bd787a799fdffe9b09350cdb617d71ef8e7205b356acbf198ea6365'