import random
import string
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import hashlib



class PasswordManager:
    def __init__(self, encryption_key):
        self.passwords = {}

        key = encryption_key
        key = key.encode('utf-8')
        hash_object = hashlib.sha256(key)
        hash_bytes = hash_object.digest()

        self.encryption_key = hash_bytes

    def add_password(self, website, username, password):
        self.passwords[website] = {'username': username, 'password': password}

    def get_password(self, website):
        if website in self.passwords:
            return self.passwords[website]['password']
        else:
            return False

    def get_username(self, website):
        if website in self.passwords:
            return self.passwords[website]['username']
        else:
            return False

    def list_websites(self):
        return list(self.passwords.keys())

    def generate_password(self, length=12, use_digits=True, use_special_chars=True):
        characters = string.ascii_letters
        if use_digits:
            characters += string.digits
        if use_special_chars:
            characters += string.punctuation

        generated_password = ''.join(random.choice(characters) for _ in range(length))
        return generated_password

    def _encrypt(self, plaintext):
        cipher = AES.new(self.encryption_key, AES.MODE_CBC)
        cipher_text = cipher.encrypt(pad(plaintext.encode('utf-8'), AES.block_size))
        return base64.b64encode(cipher.iv + cipher_text).decode('utf-8')

    def _decrypt(self, ciphertext):
        decoded_ciphertext = base64.b64decode(ciphertext)
        iv = decoded_ciphertext[:AES.block_size]
        cipher = AES.new(self.encryption_key, AES.MODE_CBC, iv=iv)
        decrypted_text = unpad(cipher.decrypt(decoded_ciphertext[AES.block_size:]), AES.block_size)
        return decrypted_text.decode('utf-8')

    def get_passwords_dict(self):
        return self.passwords

    def database_row(self, list_row):
        for id, website, username, password in list_row:
            self.add_password(website, username, password)
