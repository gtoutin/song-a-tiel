include .env

build-docker:
	docker build \
	--tag song-a-tiel-backend \
	.

run-docker:
	docker run -it -d \
	--name song-a-tiel-backend \
	-v `pwd`:/song-a-tiel \
	-w /song-a-tiel \
	-p ${PORT}:5000 \
	--env-file .env \
	song-a-tiel-backend

exec-docker:
	docker exec -it song-a-tiel-backend bash

yeet-docker:
	docker stop song-a-tiel-backend
	docker rm song-a-tiel-backend

pip-install:
	pip install -r requirements.txt