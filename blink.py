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

# print(json.dumps(res.json(), indent=4))  # 👈 Add this here
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