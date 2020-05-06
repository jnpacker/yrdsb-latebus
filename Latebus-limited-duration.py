# Copyright 2019 codingpackman & jnpacker
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
import os
import chromecast
import pandas as pd
import html5lib

with open('latebus-config.yaml', 'r') as file:
    config = yaml.load(file)

def SendNotifications (msg_type):
    print("Sending notifications")
    for webhook in config["config"]["webhook"]:
        resp = requests.post(webhook + msg_type, {})
        if resp.status_code != 200:
            print("Failed webhook: " + webhook + " status-code: " + str(resp.status_code))
    chromecast.message_cast(config["config"]["late_message"])

def checkCancel(buscity, textsearch, msg_type):
    resp = requests.get(buscity)
    print("Queried " + buscity + " and received status-code: " + str(resp.status_code))
    if resp.text.find(textsearch) > 0:
        print("my bus is " + msg_type + ": "+ str(vtime.hour) + ":" + str(vtime.minute))
        SendNotifications(msg_type)
        exit()


def checkBus(buscity, school_name, bus_number, msg_type):
    resp = requests.get(buscity)
    # Panda HTML to table library
    bus_tables = pd.read_html(resp.text)
    table = bus_tables[0]
    print("Queried " + buscity + " and received status-code: " + str(resp.status_code))
    for (idx, row) in table.iterrows():
        #if resp.text.find(textsearch) > 0: # Deprivated
        if row['School'].casefold() == school_name.casefold() and row['Route'] == bus_number:
            print("my bus is " + msg_type + ": "+ str(vtime.hour) + ":" + str(vtime.minute))
            SendNotifications(msg_type)
            exit()

attempts = 0
duration = int(os.environ["CHECK_DURATION"])
url = os.environ["CHECK_URL"]
school = os.environ["SCHOOL_NAME"]
bus_number = os.environ["BUS_NUMBER"]
#check_string = school + "</td><td>" + bus_number #Depracated

while attempts < duration:

    tz = pytz.timezone(config["config"]["timezone"])
    vtime = datetime.datetime.now(tz)

    # We look for cancelled buses first
    checkCancel(url,                                                      # URL to check
             "YORK REGION DISTRICT school boards are cancelled ",      # Search string to match
             "CANCELLED")                                              # Message
    checkBus(url+"/latebus",school, bus_number,"DELAYED")

    print("Nothing to do. Check again in 60s...")
    time.sleep(60)
    attempts = attempts + 1
print("Done. " + str(vtime.hour) + ":" + str(vtime.minute))
