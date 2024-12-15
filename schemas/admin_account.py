from pydantic import BaseModel 

class AdminAccount(BaseModel):
    id: int
    name: str
    account_id: str
    client_id: str
    client_secret: str