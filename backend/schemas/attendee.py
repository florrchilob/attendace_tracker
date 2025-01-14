from pydantic import BaseModel 
from typing import Optional
from datetime import datetime

class Attendee(BaseModel):
    id: Optional[int] = None
    mispar_ishi: Optional[str] = None
    tehudat_zehut: Optional[str] = None
    full_name: Optional[str] = None
    arrived: Optional[bool] = None
    date_arrived: Optional[datetime] = None

    def create_straight(self, data):
        self.id = data.get("id")
        self.mispar_ishi = data.get("mispar_ishi")
        self.tehudat_zehut = data.get("tehudat_zehut")
        self.full_name = data.get("full_name") 
        self.arrived = data.get("arrived")
        self.date_arrived = data.get("date_arrived")
        

    def return_dict(self):
        return {
            "id": self.id,
            "mispar_ishi": self.mispar_ishi,
            "tehudat_zehut": self.tehudat_zehut,
            "full_name": self.full_name,
            "arrived": self.arrived,
            "date_arrived": self.date_arrived.strftime("%Y-%m-%d %H:%M:%S") if self.date_arrived is not None else None
        }