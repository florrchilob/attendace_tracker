from pydantic import BaseModel 
from typing import Optional

class Attendee(BaseModel):
    id: Optional[int] = None
    mispar_ishi: Optional[int] = None
    tehudat_zehut: Optional[int] = None
    full_name: Optional[str] = None
    arrived: Optional[bool] = None

    def create_straight(self, data):
        self.mispar_ishi = data.get("mispar_ishi")
        self.tehudat_zehut = data.get("tehudat_zehut")
        self.full_name = data.get("full_name") 

    # def update_amount(self, license):
    #     self.id = license.id,
    #     self.license_id = license.license_id
    #     self.admin_account_id = license.admin_account_id
    #     self.amount_licenses = license.amount_licenses-1
