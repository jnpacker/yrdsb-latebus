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
---
### Long running docker container (Daemon)
1. Create the `latebus-config.yaml` file, by editing and saving `latebus-config-example.yaml`.
2. Build your container image from the root directory of this repository.
```bash
cp Dockerfile.template Dockerfile
echo CMD python Latebus.py >> Dockerfile
docker build . -t latebus:latest

# OR

build.bat
```
4. Run your container image with
```bash
docker run -d --restart unless-stopped --name latebus latebus
```
_**Note:** This runs the container as non-interactive. It will start with your system and uses the container name "latebus".  The last reference "latebus" is the image name created in Step 2_

---
### Limited duration docker container
1. Create the `latebus-config.yaml` file, by editing and saving the `latebus-config-example.yaml`. `morningbus` and `afternoonbus` sections are **NOT** used.
2. This container should be run once for each monitoring window. It takes four environment variables(in addition to the `latebus-config.yaml`):
- CHECK_URL       This is the URL to monitor for the bus
- CHECK_DURATION  This is how many minutes to monitor for once the container is launched
- SCHOOL_NAME     This is the name of the school
- BUS_NUMBER      This is the bus number<br><br>
_**Note:** The `SCHOOL_NAME` and `BUS_NUMBER` are concatonated together with `</td><td>` for the search term. This is because the bus numbers are used more then once for different schools in the table on School Bus City_

```
export CHECK_URL=http://net.schoolbuscity.com
export CHECK_DURATION=1
export SCHOOL_NAME=Yorkbus
export BUS_NUMBER=1111
```

3. Add the following to a scheduled task (Windows) or cronjob. <br>
```bash
docker run --name latebus -e CHECK_URL="http://net.schoolbuscity.com" -e CHECK_DURATION=60 -e SCHOOL_NAME="MYSCHOOL PS" -e BUS_NUMBER=9999 --rm latebus-limited-duration
```
_**Note:** The task will show as running for the full CHECK_DURATION value in minutes because there is no `-d` option_
