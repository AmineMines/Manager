from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import os

key_length = 16
key = get_random_bytes(key_length)
key_hex = key.hex()
os.environ["MY_ENCRYPTION_KEY"] = key_hex
encryption_key = bytes.fromhex(os.environ["MY_ENCRYPTION_KEY"])
print(f'encrypted key :{key} \n environement {encryption_key}')