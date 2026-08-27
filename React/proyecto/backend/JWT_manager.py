import jwt
from pathlib import Path
# Taken from week 7 and 8
class JWT_Manager:
    # first, to convert hs256 to RS256, you need to generate a public and private key pair
    # you can use openssl to generate these keys
    # Then, the constructor will read the keys from the specified paths
    def __init__(self, private_key_path: str, public_key_path: str):
        self.algorithm = "RS256"
        self.private_key = Path(private_key_path).read_bytes()
        self.public_key  = Path(public_key_path).read_bytes()
    # use the private key to sign the JWT in the encode method
    def encode(self, data: dict):        
        try:
            token = jwt.encode(data, self.private_key, algorithm=self.algorithm)            
            if isinstance(token, bytes):
                token = token.decode("utf-8")
            return token
        except Exception as e:
            print("JWT encode error:", e)
            return None
    # use the public key to verify the JWT in the decode method
    # if the token is valid, it will return the decoded data
    # if the token is invalid, it will return None
    def decode(self, token: str):
        
        try:
            return jwt.decode(token, self.public_key, algorithms=[self.algorithm])
        except Exception as e:
            print("JWT decode error:", e)
            return None