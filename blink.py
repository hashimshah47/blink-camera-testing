# A simple example to demonstrate the protocol:
# Download available videos
import requests
import shutil
import os
import sys
import json
import time
from datetime import datetime
import pytz
import os.path

if len(sys.argv) != 3:
    print('usage: ' + sys.argv[0] + ' email password')
    exit()

headers = {
    'Content-Type': 'application/json',
}
data = '{ "password" : "' + sys.argv[2] + '", "email" : "' + sys.argv[1] + '" }'
print(data)
# res = requests.post('https://rest-u025.immedia-semi.com/api/v5/account/login', headers=headers, data=data)
res = {
    "account": {
        "account_id": 468612,
        "country": "CA",
        "user_id": 468603,
        "client_id": 1373420,
        "client_trusted": False,
        "new_account": False,
        "tier": "u025",
        "region": "ap",
        "account_verification_required": False,
        "phone_verification_required": False,
        "client_verification_required": True,
        "require_trust_client_device": True,
        "country_required": False,
        "verification_channel": "phone",
        "user": {
            "user_id": 468603,
            "country": "CA"
        },
        "amazon_account_linked": False,
        "braze_external_id": "3610e50ae58f767d5951e54a28fb03a3853844a2836324c7a91c1e3cf6c37d6a"
    },
    "auth": {
        "token": "lTmrMTuBCoQkrLvWrD-YEA"
    },
    "phone": {
        "number": "+1******6007",
        "last_4_digits": "6007",
        "country_calling_code": "1",
        "valid": True
    },
    "verification": {
        "email": {
            "required": False
        },
        "phone": {
            "required": True,
            "channel": "sms"
        }
    },
    "lockout_time_remaining": 0,
    "force_password_reset": False,
    "allow_pin_resend_seconds": 90

}
# print(json.dumps(res.json(), indent=4))  # 👈 Add this here
authToken = "0yHSHACwAAS4F_zwiBlDPg"
# res.json()["auth"]["token"]
# region = res.json()["region"]["tier"]
accountID = 468612
# res.json()["account"]["account_id"]

print("AuthToken: %s Account ID: %i" % (authToken, accountID))

host = 'rest-u025.immedia-semi.com'
headers = {
    # 'Host': host,
    'token-auth': authToken,
}

res = requests.get('https://rest-u025.immedia-semi.com/api/v3/accounts/468612/homescreen', headers=headers)
print(json.dumps(res.json(), indent=4))  # 👈 Add this here

networkID = 716822
# str(res.json()["networks"][1]["id"])

print("Network - %s" % networkID)

fileFormat = "%Y-%m-%d %H-%M-%S"
pageNum = 1
while True:
    time.sleep(0.25)
    pageNumUrl = 'https://rest-u025.immedia-semi.com/api/v1/accounts/468612/media/changed?since=2025-04-14T23:11:20+0000&page=1'
    print("## Processing page - %i ##" % pageNum)
    res = requests.get(pageNumUrl, headers=headers)

    print(json.dumps(res.json(), indent=4))  # 👈 Add this here


    videoListJson = res.json()["media"]
    if not videoListJson:
        print(" * ALL DONE !! *")
        break
    for videoJson in videoListJson:
        # print(json.dumps(videoJson, indent=4, sort_keys=True))
        mp4Url = 'https://%s%s' % (host, videoJson["media"])
        datetime_object = datetime.strptime(videoJson["created_at"], '%Y-%m-%dT%H:%M:%S+00:00')
        utcmoment = datetime_object.replace(tzinfo=pytz.utc)
        localDatetime = utcmoment.astimezone(pytz.timezone(videoJson["time_zone"]))
        fileName = localDatetime.strftime(fileFormat) + " - " + videoJson["device_name"] + " - " + videoJson["network_name"] + ".mp4"

        if os.path.isfile(fileName):
            print(" * Skipping %s *" % fileName)
        else:
            print("Saving - %s" %fileName)
            res = requests.get(mp4Url, headers=headers, stream=True)
            with open("tmp-download", 'wb') as out_file:
                shutil.copyfileobj(res.raw, out_file)
            os.rename("tmp-download", fileName)
    pageNum += 1