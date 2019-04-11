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

with open('latebus-config.yaml', 'r') as file:
    config = yaml.load(file)

def SendNotifications (msg_type):
    print("Sending notifications")
    for webhook in config["config"]["webhook"]:
        requests.post(webhook + msg_type, {})

def Clate (start_hour, start_min, end_hour, end_min, buscity, textsearch, latebusfound, msg_type):
    if ((vtime.tm_hour == start_hour and vtime.tm_min >= start_min) or (vtime.tm_hour == end_hour and vtime.tm_min <= end_min)):
        resp = requests.get(buscity)
        if resp.text.find(textsearch) > 0:
            print("my bus is " + msg_type + ": "+ str(vtime.tm_hour) + ":" + str(vtime.tm_min))
            if latebusfound == False:
                SendNotifications(msg_type)
                return True
            else:
                print("Skipping notifications, already sent")
    return latebusfound

latebusfound = False
while True:

    vtime = time.gmtime()

    if Clate(12, 00, 13, 30, "http://net.schoolbuscity.com", "YORK REGION DISTRICT school boards are cancelled ", latebusfound, "CANCELLED"):
        latebusfound = True

    elif Clate(12, 00, 13, 30,"http://net.schoolbuscity.com/latebus", config["config"]["morningbus"],latebusfound, "DELAYED"):
        latebusfound = True

    elif Clate(20, 30, 21, 30, "http://net.schoolbuscity.com/latebus", config["config"]["afternoonbus"], latebusfound, "DELAYED"):
        latebusfound = True

    else:
        print("Did not check. Checking happens at 12:00 - 13:30 GMT and 20:30 - 21:30. Current time: " + str(vtime.tm_hour) + ":" + str(vtime.tm_min) + " GMT")
        latebusfound = False

    print("I will check again in 60s...")
    time.sleep(60)
