from pydantic import BaseModel 
from datetime import time, date
from typing import Optional


class MeetingBD(BaseModel):
    id: Optional[int] = None
    sub_account_id: Optional[int] = None
    day: date
    since: time
    until: time
    people_amount: Optional[int] = None
    confirmed: Optional[bool] = None
    licensed_now: Optional[bool] = None
    license_id: Optional[int] = None
    admin_account_id: Optional[int] = None

    def complete_meeting (self, sub_account_id, confirmed, licensed_now, license_id, admin_account_id):
        self.sub_account_id = sub_account_id
        self.confirmed = confirmed
        self.licensed_now = licensed_now
        self.license_id = license_id
        self.admin_account_id = admin_account_id

    def change_time (self, since, until):
        self.since = since
        self.until = until

    def make_jsonable(self):
        self.day = str(self.day)
        self.since = str(self.until)
        self.until = str(self.until)
        return self

