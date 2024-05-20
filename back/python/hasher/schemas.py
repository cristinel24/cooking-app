from pydantic import BaseModel

class HashData(BaseModel):
    hash: str
    salt: str | None

class PrimaryHashData(HashData):
    hashAlgorithmName: str
