import os

encryption_key = bytes.fromhex(os.environ["MY_ENCRYPTION_KEY"])
print(encryption_key)