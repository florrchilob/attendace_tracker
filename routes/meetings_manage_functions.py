import secrets
import string
import datetime
import base64
import json
from schemas.token import Token
from schemas.sub_account import SubAccount
from schemas.token import cipher
from schemas.meetingReceived import MeetingReceived
from routes.db_helpers import get_same_hours, get_all_licenses

def check_free_licenses(new_meeting: MeetingReceived):
    same_hour = get_same_hours(new_meeting)
    if (same_hour==False): 
        #error en la busqueda a BD
        return "error"
    all_licenses = get_all_licenses(new_meeting)
    licenses_left = check_licenses_left(all_licenses, same_hour)
    if (licenses_left == False):
        return "licenses"
    return licenses_left

def check_licenses_left(all_licenses, same_hours):
    free_licenses = all_licenses
    for usedLicense in same_hours:
        for index, license in enumerate(all_licenses): 
            if(usedLicense.license_id == license.id):
                license.update_amount(license)
                if(license.amount_licenses <= 0):
                    del free_licenses[index]
                    break
                free_licenses[index] = license
                break
    if(len(free_licenses) == 0):
        return False
    sorted_list = sorted(free_licenses, key=lambda x: x.license_id)
    return sorted_list[0]