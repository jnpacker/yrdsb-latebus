# This file builds the standard latebus docker container
copy Dockerfile.template Dockerfile
echo CMD python Latebus.py >> Dockerfile

docker build . -t latebus:latest
