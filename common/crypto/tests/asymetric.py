from fastapi import FastAPI
from pydantic import BaseModel

import base64
import json

from common.crypto.rsa import rsa_encrypt, rsa_decrypt

app = FastAPI(title="Asymmetric Encryption Demo")

public_key_pem = "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAm4vALpWTkxbI395ewpk8\nF/lp9pvfklzeKeK8bE7eXdihhGFuWr1Q53b0xPVbaZ50khcc3SsWCWFamSytfHaO\npdy4jrZiaLJhRROan4BHB0ePSpBJ31y24eLUfFJqSi2sQiZNDPU8O04f9uz8AhXY\nkgTMNbZYe9ntv/XJzL+b+AoK4nsP68VX9SOMKdGTj8rRhCgK4o83YqYRMch4jTEg\nwdNqYwKZa/bLIpr0OZ6+n2OIjMIrFEL/Enl2YG/7bJjSVlxKtzY5LHTB3cjyMJ1o\nmJDnusBgwT/ZBctmGxp3MlzsfzpqHAo4eyCg/vfArpUu28dyTIi3qlWIM0BF3k6Q\nLwIDAQAB\n-----END PUBLIC KEY-----\n"
private_key_pem = "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCbi8AulZOTFsjf\n3l7CmTwX+Wn2m9+SXN4p4rxsTt5d2KGEYW5avVDndvTE9VtpnnSSFxzdKxYJYVqZ\nLK18do6l3LiOtmJosmFFE5qfgEcHR49KkEnfXLbh4tR8UmpKLaxCJk0M9Tw7Th/2\n7PwCFdiSBMw1tlh72e2/9cnMv5v4Cgriew/rxVf1I4wp0ZOPytGEKArijzdiphEx\nyHiNMSDB02pjAplr9ssimvQ5nr6fY4iMwisUQv8SeXZgb/tsmNJWXEq3NjksdMHd\nyPIwnWiYkOe6wGDBP9kFy2YbGncyXOx/OmocCjh7IKD+98CulS7bx3JMiLeqVYgz\nQEXeTpAvAgMBAAECggEARpzFRICby4jq7RJek1oMGVgdPhpZ/vBQ3NP1NPgC47id\n7mJqvh+2lDWA/c7izkpkYhPDAzZ1nRGIlwPcyCVsMajHUeZDO4NLPBgfuCv8UrYu\nOyvQlWlaDqayTrP9U6pzSl5n2SuVSdj4EtlXuDyhofwylmmutp7i2yOiFmSf0hRL\nucuSNSdhoslyqdqqTQbu65e1RrIXhwLLJNGgkr+Hv31YyGG4Y6gvYu8IibGDwD12\nBDD+iJSrKRfypPaH9kji3NyIzq4qU5pTawojVDsUKJ0Re+J3+hjQCA8DckAeTiT1\ns97ehpPrzktZJ0A6WpmXVvsGjGb9Jgc++2ILIcK5JQKBgQDPGq2gUon4INEfREnw\nnoaoSdqqz2nb5WaHaYQ+5MDAESZCyvjMqOuif48dE3LR8DHwsSEYfNqzqjG256vc\nN4ChpwKjV+iDXaqt4BSLbSjPZyK9wNwoIfOVou7QL5HkeBLFg/I9mDda+iYMh9eO\nnyiM89fcE+Ka4kQA7/dAYMaJiwKBgQDAROb+8wvK679O+uad/AqgdQ/f/vtvDiSK\nOFxXL41MPboDDFRcWjM5yOynPJhAs6zGSX4j6XAMropOjMiAllulDTJ/QF7HAY4k\ne6DbcFXzIqmxsVZ8vXV4Nxx0CpvFAadsWV01cDkM3s5zn/+pHpCLVvz1Ruo9LX8G\ntpLouhIAbQKBgBr4t3n0peE5rOJsi1CZ5KGQFLlAD+JCaurhtAZY1j1tPlVeh65n\npWBhSmsX+FEc/fQBrXS59eWGGblfTIN+evMShAZv0WkiTrMcRrCtw63XGbAqqMFV\nQprPQFi+iTp+5LryZx7cbwEbKM9i9ZCua6KHsyoHMPDI3OBeYA3zTIfnAoGAWS+c\n9yZGkhpI45n+38nKJCQo+P6OIzWsPXFnZAnqwTLg1gkiGLS+jk9ldy3kch7mRhRR\nLtdZ4ogUH9uuJfeZCzbT9bMmQ6m1BbdTJnc1Z1Ls5EAenj5D/z+RM0K4fuoFf3z0\nf5VO4Wl42qmdLhW/duMi86OxhC9WfQaznsCxGQECgYA7WKfJg65cQtvg8P5MT+gd\nCuCJZu5WIcoJ1DBt9uMX40oSLMtue+ldr3WJ5sp4rtDFal+z6IIvMUQ7rDAKVpPu\n36EasXFPqJTJuvXRgh65ZOB+EAqssyZ3eOh6gMNZt3tgFkznBTuFTjrV/aCVcPFz\nxGTbY5fK85NC1s1eOIWmbQ==\n-----END PRIVATE KEY-----\n"

class EncryptRequest(BaseModel):
    email: str
    password: str

class DecryptRequest(BaseModel):
    encrypted: str

@app.post("/encrypt")
def encrypt_data(req: EncryptRequest):
    # Convert the Pydantic model to a dictionary
    data_dict = req.model_dump()

    # Convert dict to JSON string
    plaintext_str = json.dumps(data_dict)

    # Convert string to bytes for encryption
    plaintext_bytes = plaintext_str.encode()

    # Encrypt the plaintext bytes using RSA → encrypted bytes
    encrypted_bytes = rsa_encrypt(plaintext_bytes, public_key_pem)

    # Convert encrypted bytes to Base64 string for safe API transport
    encrypted_b64_str = base64.b64encode(encrypted_bytes).decode()

    return {"encrypted_base64": encrypted_b64_str}


@app.post("/decrypt")
def decrypt_data(req: DecryptRequest):
    # Extract Base64 encrypted string from request body
    encrypted_b64_str = req.encrypted

    # Decode Base64 → encrypted bytes
    encrypted_bytes = base64.b64decode(encrypted_b64_str)

    # Decrypt encrypted bytes using RSA → plaintext bytes
    decrypted_bytes = rsa_decrypt(encrypted_bytes, private_key_pem)

    # Convert plaintext bytes back to readable string
    decrypted_str = decrypted_bytes.decode()

    # Parse JSON string back into dictionary
    decrypted_dict = json.loads(decrypted_str)

    return {"decrypted": decrypted_dict}