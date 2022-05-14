include .env

build-docker:
	docker build \
	--tag song-a-tiel-backend \
	.

run-docker:
	docker run -it -d --rm \
	--name song-a-tiel-backend \
	-v `pwd`:/song-a-tiel \
	-w /song-a-tiel \
	song-a-tiel-backend bash

exec-docker: run-docker
	docker exec -it song-a-tiel-backend bash