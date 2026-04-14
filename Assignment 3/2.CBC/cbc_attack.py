from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os


key = b'sixteen_byte_key'
iv = os.urandom(16)


def encrypt(msg):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return cipher.encrypt(pad(msg.encode(), 16))

def decrypt(ct, iv_used):
    cipher = AES.new(key, AES.MODE_CBC, iv_used)
    return unpad(cipher.decrypt(ct), 16).decode()

# --- Original Message ---
msg = "admin=0;user=Samyak"
print("Before Attack (Original Plaintext):", msg)

ct = encrypt(msg)

# Normal decryption (no attack)
original = decrypt(ct, iv)
print("Decrypted (No Attack):", original)


fake_iv = bytearray(iv)

# Flip '0' → '1'
pos = msg.index('0')
fake_iv[pos] ^= ord('0') ^ ord('1')

# Decrypt with modified IV
attacked = decrypt(ct, bytes(fake_iv))
print("\nAfter Attack (Modified Plaintext):", attacked)

# Check result
if "admin=1" in attacked:
    print("SUCCESS: Admin access granted!")
else:
    print("DENIED")