options:
	printf "\ncmd> make build-limited-duration\n     make build\n"

build-limited-duration:
	cp Dockerfile.template Dockerfile
	echo CMD python Latebus.py >> Dockerfile
	docker build . -t latebus-limited-duration:latest

build:
	cp Dockerfile.template Dockerfile
	echo CMD python Latebus.py >> Dockerfile
	docker build . -t latebus:latest