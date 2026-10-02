import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

def _key(pw, salt):
    return PBKDF2HMAC(hashes.SHA256(), 32, salt, 200_000).derive(pw.encode())

def encrypt(text, pw):
    salt, nonce = os.urandom(16), os.urandom(12)
    return salt + nonce + AESGCM(_key(pw, salt)).encrypt(nonce, text.encode(), None)

def decrypt(blob, pw):
    salt, nonce, ct = blob[:16], blob[16:28], blob[28:]
    return AESGCM(_key(pw, salt)).decrypt(nonce, ct, None).decode()