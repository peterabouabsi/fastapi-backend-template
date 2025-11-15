from pydantic import BaseModel, ConfigDict

class EncrypteData(BaseModel):
    ciphertext: str
    iv: str
    
    model_config = ConfigDict(validate_by_name=False)

class EncryptedRequestData(EncrypteData):
    ...
class EncryptedResponseData(EncrypteData):
    tag: str

class EncryptedRequest(BaseModel):
    data: EncryptedRequestData
    key: str
    
    model_config = ConfigDict(validate_by_name=False)

class EncryptedResponse(BaseModel):
    data: EncryptedResponseData
    key: str
    
    model_config = ConfigDict(validate_by_name=False)