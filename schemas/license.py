from pydantic import BaseModel 

class License(BaseModel):
    id: int
    name:int
    amount_people: str
