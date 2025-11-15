from common.crypto.fernet import generate_fernet_key, encrypt_data, decrypt_data

data = {"user_id": 123, "role": "admin", "prefs": {"theme": "dark"}}
key = generate_fernet_key()
print("Secret key:", key.decode())

token = encrypt_data(data, key)
print("Encrypted token:", token)

decrypted = decrypt_data(token, key)
print("Decrypted data:", decrypted)