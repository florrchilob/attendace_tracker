import secrets
import string
import datetime
import base64
import json
from schemas.token import Token
from schemas.sub_account import SubAccount
from schemas.token import cipher

#Generates a token (Token class)
def token_generate():
    characters = string.ascii_letters + string.digits
    token = ''.join(secrets.choice(characters) for _ in range(16))
    refresh_token = ''.join(secrets.choice(characters) for _ in range(16))
    expiration = datetime.datetime.now() + datetime.timedelta(days = 1)
    token_return = Token(token = token, refresh_token = refresh_token, expiration = expiration)
    return token_return

#Decode token to Token type
def token_decode(encoded_token):
#     decoded_token = cipher.decrypt(encoded_token)
#     print(decoded_token)
#     # token_json = json.loads(decoded_token)
#     # expiration_datetime = datetime.datetime.strptime((token_json.get("expiration")), "%Y-%m-%d %H:%M:%S")
#     # token_to_return = Token(token = token_json.get("token"), refresh_token = token_json.get("refresh_token"), expiration = expiration_datetime)
#     # return token_to_return
    return ""

#Complete all data of a Sub account
def complete_account(account: SubAccount, token: Token):
    setattr(account, "account_type", 0)
    setattr(account, 'validated', False)
    setattr(account, 'authorized', False)
    setattr(account, "token", token.token)
    setattr(account, "refresh_token", token.refresh_token)
    setattr(account, "token_expiration", token.expiration)
    return account
