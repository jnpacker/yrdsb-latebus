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
### Long running Daemon
1. Create the latebus-config.yaml file, by editing saving latebus-config-example.yaml
2. Build your container image with `docker build . -t latebus:latest` from the root directory of this repository. (Alternately run `build.bat`)
3. Run your container image with `docker run -d --restart unless-stopped --name latebus latebus`
```
This runs the container as non-interactive, will start with your system and uses the container name "latebus".  The last reference "latebus" is the image name created in the step 2 build.

### Limited-duration docker container
1. This container should be run once for each monitoring window. It takes four environment variables(in addition to the latebus-config.yaml):
- CHUCK_URL       This is the URL to monitor for the bus
- CHECK_DURATION  This is how many minutes to monitor for once the container is launched
- SCHOOL_NAME     This is the name of the school
- BUS_NUMBER      This is the bus number

2. _The SCHOOL_NAME and BUS_NUMBER are concat'd together with </td><td> for the search term. This is because the bus numbers are used more then once for different schools in the table on School Bus City_

3. Add the following to a Scheduled task `docker run --name latebus -e CHECK_URL="http://net.schoolbuscity.com" -e CHECK_DURATION=60 -e SCHOOL_NAME="MYSCHOOL PS" -e BUS_NUMBER=9999 --rm latebus-limited-duration`

_The task will show as running for the full CHECK_DURATION value in minutes._