from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from cryptography.fernet import Fernet
import json
import base64


key = Fernet.generate_key()
cipher = Fernet(key)

class Token(BaseModel):
    token: Optional[str] = None
    refresh_token: Optional[str] = None
    expiration: Optional[datetime] = None

    #Encode token to string
    def token_encode_JWT(self, data):
        expiration_str = self.expiration.strftime("%Y-%m-%d %H:%M:%S")
        token_data = {
            "token" : self.token,
            "refresh_token" : self.refresh_token,
            "expiration" : expiration_str
        }
        token_json = json.dumps(token_data).encode()
        token_encrypted = cipher.encrypt(token_json)
        return token_encrypted
