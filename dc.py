import base64
import hashlib
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2

# Constants for AES encryption
SALT_BYTES = bytes([
    102, 51, 111, 51, 75, 45, 49, 49, 61, 71, 45, 78,
    55, 86, 74, 116, 111, 122, 79, 87, 82, 114, 61, 40,
    116, 78, 90, 66, 102, 75, 43, 98, 83, 55, 70, 121
])

CRYPT_KEY = bytes([
    59, 38, 75, 70, 33, 77, 33, 104, 56, 94, 105, 84,
    58, 60, 41, 97, 63, 126, 109, 88, 101, 78, 42, 126,
    111, 63, 103, 78, 91, 118, 64, 114, 81, 61, 66
])

def decrypt(encrypted_value):
    # Decode the Base64 encoded string
    encrypted_bytes = base64.b64decode(encrypted_value)

    # Derive the key and IV using PBKDF2
    key_iv = PBKDF2(CRYPT_KEY, SALT_BYTES, dkLen=32 + 16, count=1000)
    key = key_iv[:32]  # AES key size 256 bits
    iv = key_iv[32:]   # AES block size 128 bits

    # Decrypt using AES in CBC mode
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_bytes = cipher.decrypt(encrypted_bytes)

    # Unpad the decrypted bytes
    padding_length = decrypted_bytes[-1]
    decrypted_bytes = decrypted_bytes[:-padding_length]

    return decrypted_bytes.decode('utf-8')

def decrypt_config(encrypted_string):
    if not encrypted_string.startswith("ENCRYPTED:"):
        return encrypted_string
    return decrypt(encrypted_string.replace("ENCRYPTED:", ""))

# Encrypted values
telegram_bot_api = decrypt_config("ENCRYPTED:BncRbgTGet4L+mKqD8dz7h8EdEcrI2Pbm5InYO5Ff/I=")
zulip_api_base_url = decrypt_config("ENCRYPTED:hu7mPNLn8F3W1m8DcwM5LXHInCJglBwFsWCfcHCJ9tF7oYejzA1wmRf7U4KxfmKxWUHNJ/cIv306TuGoVjZvAA==")
zulip_email = decrypt_config("ENCRYPTED:CPB7ti0A5zas/0dF4XBKzDiUIfmQ5RgrLQvDrYCST4M=")
zulip_api_key = decrypt_config("ENCRYPTED:cYs6KSRyO3yMrWGQDOmKxivjCVxRHP8X2elXQtdRGbiad1fFkV3DBIHK2EbuIBDA")

# Output the decrypted values
print("Telegram Bot API:", telegram_bot_api)
print("Zulip API Base URL:", zulip_api_base_url)
print("Zulip Email:", zulip_email)
print("Zulip API Key:", zulip_api_key)
