# Copyright 2019 codingpackman
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import requests as requests
import time
import yaml
import pytz
from pytz import timezone
import datetime

with open('latebus-config.yaml', 'r') as file:
    config = yaml.load(file)

def SendNotifications (msg_type):
    print("Sending notifications")
    for webhook in config["config"]["webhook"]:
        resp = requests.post(webhook + msg_type, {})
        if resp.status_code != 200:
            print("Failed webhook: " + webhook)

def Clate (start_hour, start_min, end_hour, end_min, buscity, textsearch, latebusfound, msg_type):
    if (vtime.hour == int(start_hour) and vtime.minute >= int(start_min)) or (vtime.hour == int(end_hour) and vtime.minute <= int(end_min)):
        resp = requests.get(buscity)
        if resp.text.find(textsearch) > 0:
            print("my bus is " + msg_type + ": "+ str(vtime.hour) + ":" + str(vtime.minute))
            if latebusfound == False:
                SendNotifications(msg_type)
                return True
            else:
                print("Skipping notifications, already sent")
    return latebusfound

latebusfound = False

while True:

    tz = pytz.timezone(config["config"]["timezone"])
    vtime = datetime.datetime.now(tz)

    config["config"]["morningbus"]["start"].split(":",1)[0]

    if Clate(config["config"]["morningbus"]["start"].split(":",1)[0],  # Morning bus start time HR
             config["config"]["morningbus"]["start"].split(":",1)[1],  # Morning bus start time MIN
             config["config"]["morningbus"]["stop"].split(":",1)[0],   # Morning bus stop time HR
             config["config"]["morningbus"]["stop"].split(":",1)[1],   # Morning bus stop time MIN
             "http://net.schoolbuscity.com",                           # URL to check
             "YORK REGION DISTRICT school boards are cancelled ",      # Search string to match
             latebusfound, "CANCELLED"):                               # Toggle identifying if already matched, so we don't notify more then once
        latebusfound = True

    elif Clate(config["config"]["morningbus"]["start"].split(":",1)[0],  # Morning bus start time HR
             config["config"]["morningbus"]["start"].split(":",1)[1],  # Morning bus start time MIN
             config["config"]["morningbus"]["stop"].split(":",1)[0],   # Morning bus stop time HR
             config["config"]["morningbus"]["stop"].split(":",1)[1],   # Morning bus stop time MIN
             "http://net.schoolbuscity.com/latebus", config["config"]["morningbus"]["bus_check"],latebusfound, "DELAYED"):
        latebusfound = True

    elif Clate(config["config"]["afternoonbus"]["start"].split(":",1)[0],  # Morning bus start time HR
             config["config"]["afternoonbus"]["start"].split(":",1)[1],  # Morning bus start time MIN
             config["config"]["afternoonbus"]["stop"].split(":",1)[0],   # Morning bus stop time HR
             config["config"]["afternoonbus"]["stop"].split(":",1)[1],   # Morning bus stop time MIN
              "http://net.schoolbuscity.com/latebus", config["config"]["afternoonbus"]["bus_check"], latebusfound, "DELAYED"):
        latebusfound = True

    else:
        print("Did not check. Checking happens at " + str(config["config"]["morningbus"]["start"]) + " - " + str(config["config"]["morningbus"]["stop"]) + " and " + str(config["config"]["afternoonbus"]["start"]) + " - " + str(config["config"]["afternoonbus"]["stop"]) + ". Current time: " + str(vtime.hour) + ":" + vtime.strftime("%M") + " " + str(tz))
        latebusfound = False

    print("I will check again in 60s...")
    time.sleep(60)
