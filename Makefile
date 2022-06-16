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
	-p 5000:5000 \
	--entrypoint '' \
	song-a-tiel-backend bash

exec-docker:
	docker exec -it song-a-tiel-backend bash

yeet-docker:
	docker stop song-a-tiel-backend
	docker rm song-a-tiel-backend

pip-install:
	pip install -r requirements.txt