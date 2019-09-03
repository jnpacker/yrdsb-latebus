# YRDSB Latebus Notifications
You can find your late bus
1. Create a config file named `latebus-config.yaml`.
2. The file should contain the following:
```
config:
  timezone: "US/Eastern"
  webhook:
  - "https://maker.ifttt.com/trigger/goingtobelate/with/key...........?value1="
  morningbus:
    bus_check: "MYSCHOOL PS</td><td>9999"
    start: "7:00"
    stop: "8:00"
  afternoonbus:
    bus_check: "MYSCHOOL PS</td><td>1111"
    start: "15:00"
    stop: "16:30"
```
_**Note:** You must create an IFTTT webhook to notify or text you_

3. The webhook entry is an array to support multiple hooks
4. This program is ready to be pushed in Cloud Foundry using the Python Buildpack
5. Command from the repository's root directory:
```
cf push latebus --no-route -u process
```

## IFTTT Webhooks
Setup your IFTTT webhooks here: https://ifttt.com/maker_webhooks

## Run as a docker container
1. Create the latebus-config.yaml file, by editing saving latebus-config-example.yaml
2. Build your container image with `docker build . -t latebus:latest` from the root directory of this repository
3. Run your container image with `docker run -d --restart unless-stopped --name latebus latebus`
```
This runs the container a non-interactive, will start with your system and uses the container name "latebus".  The last reference "latebus" is the image name created in the step 2 build.