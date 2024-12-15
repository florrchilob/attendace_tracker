from pydantic import BaseModel 
from typing import Optional
from datetime import datetime


class SubAccount(BaseModel):
    id: Optional[int] = None
    mail: Optional[str] = None
    password: Optional[str] = None
    name:  Optional[str] = None
    mispar_ishi: Optional[int] = None
    telephone: Optional[int] = None
    account_type: Optional[int] = None
    validated: Optional[bool] = None
    authorized: Optional[bool] = None
    token: Optional[str] = None
    refresh_token: Optional[str] = None
    token_expiration: Optional[datetime] = None



    def create_straight(self, data):
        self.id = data.get('id', None)
        self.mail = data.get('mail', None)
        self.password = data.get('password', None)
        self.name = data.get('name', None)
        self.mispar_ishi = data.get('mispar_ishi', None)
        self.telephone = data.get('telephone', None)
        self.account_type = data.get('account_type', None)
        self.validated = data.get('validated', None)
        self.authorized = data.get('authorized', None)
        self.token = data.get('token', None)
        self.refresh_token = data.get('refresh_token', None)
        self.token_expiration = data.get('token_expiration', None)

    def update_token (self, new_token):
        self.id = self.id
        self.mail = self.mail
        self.password = self.password
        self.name = self.name
        self.mispar_ishi = self.mispar_ishi
        self.telephone = self.telephone
        self.account_type = self.account_type
        self.validated = self.validated
        self.authorized = self.authorized
        self.token = new_token.token
        self.refresh_token = new_token.refresh_token
        self.token_expiration = new_token.expiration
