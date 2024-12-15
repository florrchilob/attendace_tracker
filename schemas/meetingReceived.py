from pydantic import BaseModel 
from datetime import time, date, datetime
from typing import Optional, Union


class MeetingReceived(BaseModel):    
    account_id: Optional[int] = None
    day: Optional[date] = None
    since: Optional[time] = None
    until: Optional[time] = None
    people_amount: Optional[int] = None

    def complete_meeting (self, zoom_id, confirmed, licensed_now, license_type_needed):
        self.zoom_id = zoom_id
        self.confirmed = confirmed
        self.licensed_now = licensed_now
        self.license_type_needed = license_type_needed

    def change_time (self, since, until):
        self.since = since
        self.until = until

    def make_jsonable(self):
        self.day = str(self.day)
        self.since = str(self.until)
        self.until = str(self.until)
        return self

    def create_straight(self, data):
        self.account_id = data.get('account_id')
        self.day = data.get('day')
        self.since = data.get('since')
        self.until = data.get('until')
        self.people_amount = data.get('people_amount')