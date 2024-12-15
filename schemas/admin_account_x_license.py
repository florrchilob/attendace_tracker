from pydantic import BaseModel 
from typing import Optional

class atrendees(BaseModel):
    id: Optional[int] = None
    mispar_hishi: Optional[int] = None
    full_name: Optional[str] = None
    arrived: Optional[bool] = None


    # def update_amount(self, license):
    #     self.id = license.id,
    #     self.license_id = license.license_id
    #     self.admin_account_id = license.admin_account_id
    #     self.amount_licenses = license.amount_licenses-1
