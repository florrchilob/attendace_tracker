from pydantic import BaseModel 
from typing import Optional

class AdminAccountXLicense(BaseModel):
    id: Optional[int] = None
    license_id: int
    admin_account_id: int
    amount_licenses: int

    def update_amount(self, license):
        self.id = license.id,
        self.license_id = license.license_id
        self.admin_account_id = license.admin_account_id
        self.amount_licenses = license.amount_licenses-1
