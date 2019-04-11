# YRDSB Latebus Notifications
You can find your late bus
1. Create a config file named `latebus-config.yaml`.
2. The file should contain the following:
```
config:
  webhook:
  - "https://maker.ifttt.com/trigger/goingtobelate/with/key...........?value1="
  morningbus: "MYSCHOOL PS</td><td>9999"
  afternoonbus: "MYSCHOOL PS</td><td>1111"
```
_**Note:** You must create an IFTTT webhook to notify or text you_

3. The webhook is an array
4. This program is ready to be pushed in Cloud Foundry using the Python Buildpack
5. Command from the repository's root directory:
```
cf push latebus --no-route -u process
```
