# This file builds the limited-duration docker container
copy Dockerfile.template Dockerfile
echo CMD python Latebus-limited-duration.py >> Dockerfile

docker build . -t latebus-limited-duration:latest
