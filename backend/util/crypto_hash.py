import hashlib
import json #Used to convert any JSON data to string.
#Probably uneeded but using JavaScript we might need to convert JSON texts.

def crypto_hash(*args): # '*' tag suggest that the we can enhance a function to take any number of args.
    """
    Tries to return the SHA-256 hash value of the given arguments. Now there is a use of JSON and Hashlib
    to convert the given string to it's SHA-256 encrypted value. Now utilising JSON ensures that we can 
    convert any form of text into a string representation which can be encoded using the UTF-8 format.
    This is then later utilised to convert that value to it's hash value. Now python has a hash function on 
    it's own but we are not using this because Python's hash returns only an intger output.
    """
    #print(f'args: {args}')

    stringified_args = sorted(map(lambda data: json.dumps(data),args)) 
    #This is done to ensure that we get the same input irrespective of the order of the same data.

    #print(f'stringified_data: {stringified_args}')
    #Print the string data

    #Generates a list with the use of one line function Lambda and using map keyword to return a list
    joined_data = ''.join(stringified_args)

    #print(f'joined_data: {joined_data}')
    

    return hashlib.sha256(joined_data.encode('utf-8')).hexdigest()

    #This will return a memory address without a hexdigest method
    #Please note that this will require encoding of the data into byte-string (Specifically 8-bit)

def main():
    print(f"crypto_hash(2,'one',[2300,3210,42390]): {crypto_hash(2,'one',[2300,3210,42390])}")

if __name__ == '__main__':
    main()