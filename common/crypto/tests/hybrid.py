
import json

from fastapi import FastAPI

from pydantic import BaseModel

from common.crypto.hybrid import hybrid_encrypt, hybrid_decrypt

app = FastAPI(title="Asymmetric Encryption Demo")

class ClientEncryptRequest(BaseModel):
    email: str
    password: str

class ClientDecryptRequest(BaseModel):
    encrypted_aeskey: str
    ciphertext: str
    nonce: str
    tag: str

class ServerEncryptRequest(BaseModel):
    status: int
    message: str

class ServerDecryptRequest(BaseModel):
    encrypted_aeskey: str
    ciphertext: str
    nonce: str
    tag: str

s_public_key = "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAuc8NJ/8JRGR5deYN4+e7\nz68XyQl1MR4nSohILn8I+zbAgchubUkXm61artXce5aAsw63eFYr1iquxMdAtbR6\nVrpUU40t46aDHrZZcV7g2Wl39lq9pIol/ZBoxU/Qa0QHj9rHCsTmSfZLehuxJdks\nrj79qok79c8AcN1g3XmvrxPVfigYCQVVAxjwfXz1NSDiTwrz8U/vu64d+13dMDTZ\nstWeGCgkcjWFKHKuL630mhZPx/qZozpC30Qvh41a3MM5kKMv/gl5Te1N0xBfA+PN\nfebJ4GI7X6fOAhZUkuHj7YNTibB+OFspBbltAFggxt+6u0kDye51Iszm6xYQ4C/7\nxwIDAQAB\n-----END PUBLIC KEY-----\n"
s_private_key = "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC5zw0n/wlEZHl1\n5g3j57vPrxfJCXUxHidKiEgufwj7NsCByG5tSRebrVqu1dx7loCzDrd4VivWKq7E\nx0C1tHpWulRTjS3jpoMetllxXuDZaXf2Wr2kiiX9kGjFT9BrRAeP2scKxOZJ9kt6\nG7El2SyuPv2qiTv1zwBw3WDdea+vE9V+KBgJBVUDGPB9fPU1IOJPCvPxT++7rh37\nXd0wNNmy1Z4YKCRyNYUocq4vrfSaFk/H+pmjOkLfRC+HjVrcwzmQoy/+CXlN7U3T\nEF8D48195sngYjtfp84CFlSS4ePtg1OJsH44WykFuW0AWCDG37q7SQPJ7nUizObr\nFhDgL/vHAgMBAAECggEAKJQTyvbTJskMj5dw1CNxLD+QYbq7icEMkqXloaXjp71C\n2HUVzK8oRTrcMY+KCcGKFNCzd8fV5f1HUrkzJBuolhU2QlL0QSHFw+jN6sjuMPzs\nEnSpsuvqtRAbGXA/U5W1UxDT5EGxC1kLDb1LeDkQHXOrQVmcKygMcBmgxG2FVSYO\n7Oh7dPKKStCTnkNGYZ4OC+gLX3VxwAazqgwdYvm4ZUPZGkBnrUcQhce0tFDkSf/g\nbdq45bg8RI8trgossMVxCmKWr7+COgzcmu8DWXhinywDfDMd3NvFALqteGFQLJk8\nH/wgYu2lnVJDnT05XWpCe23quvrrvQeCOstYbumTvQKBgQD84mDRdMA3yQvCPRMh\nfi0QCF/1euj3ZpzjgHgWKAHnbB1P7j2qsmClWLFt2JZ2k9rC/qxdBkAG28QMxGyG\nnYOwU6GpzDaQrEA1Ulmhw7jOB4YOctczTDyXegt/Jpr1kxZC50avkk4UsPY119Kz\nLeyBPAKPYvUWK2g2UVHNguLJ3QKBgQC8GRxK34lIvPlKyIyWNsd4DrMXcN6gcpuP\nFmgLtuTo+b2+xCRNxa9es212ZIgfGAkezqs5V0xjHf3Irp11NVPpgaADziOc5jKW\nqypMczGfiUpV4fSPgO9sXFn1t0dlKBzwRh1alRgYwjGxPgYMPSwkIylneypLpBUr\nwuwMKYdr8wKBgQDXmxr4+hW4ekzwOqpI8A7zkHBgF37xECfLQAkiutGEwgTr1S/2\njUchMlF0WilOyBjID+JdHasRLeYlDIOK8lkIyQUYg+gxyOqli6Sn6vtxjbCaOQeJ\n0QIIFCIhMoUDw3hDanQ11QOFWKtSlMQryIfQV53HKpPTZwbe6M5Z7bH2cQKBgCDD\nIulrrAbOW4GKEuqrGe0wakM/9pbtv2iZ13+K2K43qbQLh+M/9n7BM+S2N/tqfVQv\nXSV8riJpe+WzfFuI8Vevq0ZeZleSxOb3Y0OzoMYP7LGuzKEeLRWrtEOXK8lTxk6X\nd89qPqs5T9x2WClTkletBC4xBrnsF3/q0KCBr0O/AoGBAK2mtiwXuoA6PafsGq+0\nGSaiWQVUc9InZ99zmkvVKbfp4d9iPT6lOt1CrjXQUzkHJY7rI5tuxHvKposXAZpL\n/c9lUK85jL2NfuiCQSicjb2gseCTL0audKJXMa635xEHvCrAlHAYjqHeh5CtrN42\n+zmBKAgjwhQKDp9VhOf3xdZ0\n-----END PRIVATE KEY-----\n"

c_public_key = "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAqx2RObwbqWavlNvXt1KR\n4OM7U/uWX4tcB3wK6XsfKe9oWCEcQLgR6Rh1zAxFgfIX/Eb1SW30wQudCv7hWPhn\nQSvkF8JuEJguhfmHGvbHQ2pkuXx6pKvHMATGOPYK9z+Ik8TCnTBI8Nrhprgckkla\nu1oW1ijZmbgqhyNPZWMQPUzfUj3M2X3YEVfnWFUcsjx7Y1W+kD3w3yxPZl8EIZ36\nOawcwYIRmo5h5yfdRcLMUTdMHMhOmy8vnuJVqN/QXMHpEWTS5l3+Dr9W1LMkQVii\nFOUI4mnlg3Rn8W1/ZsTM9K70NnfagRry1ZD7k8psJ76lZwRIzd8hPr2C7LTZxeql\nBwIDAQAB\n-----END PUBLIC KEY-----\n"
c_private_key = "-----BEGIN PRIVATE KEY-----\nMIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQCrHZE5vBupZq+U\n29e3UpHg4ztT+5Zfi1wHfArpex8p72hYIRxAuBHpGHXMDEWB8hf8RvVJbfTBC50K\n/uFY+GdBK+QXwm4QmC6F+Yca9sdDamS5fHqkq8cwBMY49gr3P4iTxMKdMEjw2uGm\nuBySSVq7WhbWKNmZuCqHI09lYxA9TN9SPczZfdgRV+dYVRyyPHtjVb6QPfDfLE9m\nXwQhnfo5rBzBghGajmHnJ91FwsxRN0wcyE6bLy+e4lWo39BcwekRZNLmXf4Ov1bU\nsyRBWKIU5QjiaeWDdGfxbX9mxMz0rvQ2d9qBGvLVkPuTymwnvqVnBEjN3yE+vYLs\ntNnF6qUHAgMBAAECggEABb8rdm3r2+eX8/7iIsUCIzRedLaZWUIb6CBxWWAKLuVc\ncsFB6qaD63kn05+B4hhYV9+mMz4fHzCdqJXgyZUmGpk3wtiDy8jgnx0/PVeWX5w+\nH8CfedJPETzHz3fr7FvU4WmVQ6Qwfu5K78d1JjCSfIJNDAo5LKFzxDAaZYRLMlPJ\ngM1VC8VM34FwcslzJUlPKCxXPGHcCUHEYPolFqEh+D//jUMqS7UzL+yLCo1jSVna\nLnfZXq0aA6FfpRU8UNz/ObklS42DLuO+SB3dcyVdU5/XWAyRlSnCS28U1KfNrKHn\nh8hmOnnbjtbgl3NZIHnRomWNzLF9sbE1iO53vAOdEQKBgQDgMZN1Y8KbAgG9vrdo\nKygutNOGpo45vlX4HgrYSlQhX9yrqKdYAsNxaxieH8Afb28SdJkc7lb/ZmEJEj/v\nF1kSZjZHeYJFYs7UzzeF/vdnqd49oP88IARnvqhPuOppO4MA2Xxka9qo9DE3JSvm\nqirSZTDZc+W9kpQweHKH/ezmPwKBgQDDZELXvRseubINqL+POPtbg2pxhNV3ubFH\nugUSgu/8R/XY7qqfq5/M4Qx1kiEq4HyPsI4fWnEOhZLyRzK77IL/hru+Z4fGlQjp\nyXMPxv7kAB4PT2JUg0RUu9te7pB+bJJmx6W9KdP/0129alKeolaEAc3UR8vAHkYG\nQRT/QsZfOQKBgQCz5LPo7wqZbMvO4Di02mRczfYpRn47MVI0TI7xLPtC6HPePe9B\nfL4sxP20688yqizbBzpQ76JZP2I/cChjBj4PuHp3cbWpTXafZkKsP4Fv6esNUqFb\nMmm2gVL23W8iz4D37ouU3MJQ7diL4kTOyt6fgljnM8s2CWblWdC09Hjh6wKBgQCz\n9Pu7R2ha/ByJiAomFw0qU/cNZpJVGqm0rhdN3Vq6uGwtyGNNe/xJ7lxTTKtPmkIe\n9TVwmxPVlCCrE/geLM7aGXWBAEmFFG6JJAjdVyIbTCBjaXHe9KdSg1KgNIjQZ57P\nGsIDXyrqS/niIrLFeC7GlgLEqPt3jmpgCEEWeKHLwQKBgQCDKF3e4I18+Qz2vLbp\nMu3pL0HihTmmkWfahZYt+61FedHz6PdYR6H1wS7syXmrp7g5+qjQc0C7dSKBAMYN\nXnIaATFySxBLOyw5F+jYvGGRQXKIuzFj7Zk/hIk3C5r811kSrEW28uD42lduaund\nH7pU3Q024g6vWdh6OYe5AYIkGA==\n-----END PRIVATE KEY-----\n"

# -------------------------------
# Client encrypts → server decrypts
# -------------------------------
@app.post("/client/encrypt")
def client_encrypt(req: ClientEncryptRequest):
    # Convert the Pydantic model to a dictionary
    data_dict = req.model_dump()

    # Convert dict to JSON string
    plaintext_str = json.dumps(data_dict)

    # Convert string to bytes for encryption
    plaintext_bytes = plaintext_str.encode()
    
    encrypted = hybrid_encrypt(s_public_key, plaintext_bytes)
    return encrypted

@app.post("/server/decrypt")
def server_decrypt(req: ClientDecryptRequest):
    data = {
        "encrypted_aeskey": req.encrypted_aeskey,
        "ciphertext": req.ciphertext,
        "nonce": req.nonce,
        "tag": req.tag
    }
    plaintext_bytes = hybrid_decrypt(s_private_key, data)

    return {"decrypted": json.loads(plaintext_bytes)}

# -------------------------------
# Server encrypt → client decrypt
# -------------------------------
@app.post("/server/encrypt")
def server_encrypt(req: ServerEncryptRequest):
    # Convert the Pydantic model to a dictionary
    data_dict = req.model_dump()

    # Convert dict to JSON string
    plaintext_str = json.dumps(data_dict)

    # Convert string to bytes for encryption
    plaintext_bytes = plaintext_str.encode()
    
    encrypted = hybrid_encrypt(c_public_key, plaintext_bytes)
    return encrypted

@app.post("/client/decrypt")
def client_decrypt(req: ServerDecryptRequest):
    data = {
        "encrypted_aeskey": req.encrypted_aeskey,
        "ciphertext": req.ciphertext,
        "nonce": req.nonce,
        "tag": req.tag
    }
    plaintext_bytes = hybrid_decrypt(c_private_key, data)
    data_dict = json.loads(plaintext_bytes)
    
    return {"decrypted": data_dict}