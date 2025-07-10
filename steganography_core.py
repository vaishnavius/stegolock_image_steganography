# steganography_core.py

import cv2
import numpy as np
from Crypto.Cipher import AES
from Crypto import Random
import base64
import hashlib

def msgtobinary(msg):
    if isinstance(msg, str):
        return ''.join(format(ord(i), "08b") for i in msg)
    elif isinstance(msg, bytes) or isinstance(msg, np.ndarray):
        return [format(i, "08b") for i in msg]
    elif isinstance(msg, int) or isinstance(msg, np.uint8):
        return format(msg, "08b")
    else:
        raise TypeError("Input type not supported")

def encrypt(msg, key):
    key = hashlib.sha256(key.encode()).digest()
    msg = msg + (16 - len(msg) % 16) * chr(16 - len(msg) % 16)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return base64.b64encode(iv + cipher.encrypt(msg.encode())).decode()

def encode_image(img, message, encryption_key, stego_key, output_path):
    encrypted_msg = encrypt(message, encryption_key)
    payload = stego_key + encrypted_msg + "*^*^*"
    binary_payload = msgtobinary(payload)
    data_len = len(binary_payload)

    data_index = 0
    for row in img:
        for pixel in row:
            for i in range(3):
                if data_index < data_len:
                    pixel[i] = int(msgtobinary(pixel[i])[:-1] + binary_payload[data_index], 2)
                    data_index += 1
    cv2.imwrite(output_path, cv2.cvtColor(img, cv2.COLOR_RGB2BGR))

def decode_image(img, stego_key, decryption_key):
    binary_data = ""
    for row in img:
        for pixel in row:
            for i in range(3):
                binary_data += format(pixel[i], "08b")[-1]

    all_bytes = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    decoded_data = ""
    for byte in all_bytes:
        decoded_data += chr(int(byte, 2))
        if decoded_data.endswith("*^*^*"):
            break

    payload = decoded_data[:-5]

    # Fix: Strip both keys before comparison
    if not payload.startswith(stego_key.strip()):
        return "❌ Incorrect stego key."

    encrypted_msg = payload[len(stego_key):]

    # Decrypt
    def decrypt(enc, key):
        from Crypto.Cipher import AES
        from Crypto import Random
        import hashlib
        import base64

        key = hashlib.sha256(key.encode()).digest()
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted = cipher.decrypt(enc[16:])
        padding_len = decrypted[-1]
        return decrypted[:-padding_len].decode()

    return decrypt(encrypted_msg, decryption_key)

