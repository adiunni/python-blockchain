from backend.util.hex_to_bin import hex_to_bin

def test_hex_to_bin():
    number = 451
    hex_num = hex(number)[2:]
    bin_num = hex_to_bin(hex_num)
    assert int(bin_num,2) == number