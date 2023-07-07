from base64 import b64decode, b64encode
from typing import Tuple

from app.core.config import settings
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


def generate_task_access_key(user_id: int, task_id: int) -> str:
    # Combine the user_id and task_id to form the data to be encrypted
    data_string = f"{user_id}:{task_id}"
    # need to convert to bytes for AES encryption
    data = data_string.encode('utf-8')
    key = settings.TASK_SECRET_KEY.encode('utf-8')
    # Create cipher
    cipher = AES.new(key, AES.MODE_CBC)  # using AES-256, the key is 32 bytes
    # pad is to fill empty bytes if the data is not 16 bytes
    ct_bytes = cipher.encrypt(pad(data, AES.block_size))
    iv = cipher.iv
    result = iv + ct_bytes
    # convert bytes to base64 string to ensure it can be safely transmitted or stored without risk of modification or data loss
    return b64encode(result).decode('utf-8')


def decipher_task_access_key(access_key: str) -> Tuple[int, int]:
    key = settings.TASK_SECRET_KEY.encode('utf-8')
    # Convert base64 string to bytes
    raw = b64decode(access_key)
    # Extract the IV and ciphertext from the raw bytes
    iv = raw[:AES.block_size]  # AES block size is 16
    ciphertext = raw[AES.block_size:]
    # Create cipher
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    # Decrypt the ciphertext and remove tailing empty bytes
    data = unpad(cipher.decrypt(ciphertext), AES.block_size)
    data_string = data.decode('utf-8')
    user_id, task_id = map(int, data_string.split(':'))

    return user_id, task_id
