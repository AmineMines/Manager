from Model import PasswordManager
from Crypto.Random import get_random_bytes
import os

p = PasswordManager.PasswordManager("wmk6Px2hnGAd")
p._encrypt("test")


print(p._decrypt(p._encrypt("test")))
