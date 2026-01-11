from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

def encrypt_aes(plain_text, secret_key):
    try:
        key = secret_key.ljust(16)[:16].encode('utf-8')
        cipher = AES.new(key, AES.MODE_ECB)
        padded_data = pad(plain_text.encode('utf-8'), AES.block_size)
        ct_bytes = cipher.encrypt(padded_data)
        
        ciphertext = base64.b64encode(ct_bytes).decode('utf-8')
        return {"ciphertext": ciphertext}
    except Exception as e:
        return {"error": str(e)}

def decrypt_aes(ciphertext, secret_key):
    try:
        key = secret_key.ljust(16)[:16].encode('utf-8')
        cipher = AES.new(key, AES.MODE_ECB)
        ct_bytes = base64.b64decode(ciphertext)
        

        decrypted_padded = cipher.decrypt(ct_bytes)
        pt_bytes = unpad(decrypted_padded, AES.block_size)
        return pt_bytes.decode('utf-8')
    except Exception as e:
        return f"Error: Padding is incorrect (Cek Key atau Ciphertext anda)"