from backend.util.crypto_hash import crypto_hash

HEX_TO_BIN_CONVERSION_TABLE = {
    '0':'0000',
    '1':'0001',
    '2':'0010',
    '3':'0011',
    '4':'0100',
    '5':'0101',
    '6':'0110',
    '7':'0111',
    '8':'1000',
    '9':'1001',
    'a':'1010',
    'b':'1011',
    'c':'1100',
    'd':'1101',
    'e':'1110',
    'f':'1111',
}

def hex_to_bin(hex_string):
    """
    Converts the following hexadecimal value to binary value with the help of the 
    conversion table given below in HEX_TO_BIN_CONVERSION_TABLE.
    """
    bin_string = ''
    for char in hex_string:
        bin_string += HEX_TO_BIN_CONVERSION_TABLE[char]
    
    return bin_string

def main():
    number = 451
    hex_num = hex(number)[2:]
    print(f'Hex number : {hex_num}')

    bin_num = hex_to_bin(hex_num)
    print(f'Binary Number: {bin_num}')

    orig_num = int(bin_num,2)
    print(f'Original number: {orig_num}')

    hex_to_bin_crypt = hex_to_bin(crypto_hash("test-data"))
    print(f'hex_to_bin_crypt: {hex_to_bin_crypt}')

if __name__ == '__main__':
    main()