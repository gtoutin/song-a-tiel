build-docker:
	docker build \
	--tag song-a-tiel-backend \
	.

run-docker:
	include .env
	docker run -it -d \
	--name song-a-tiel-backend \
	-v `pwd`:/song-a-tiel \
	-w /song-a-tiel \
	-p 5000:5000 \
	--env-file .env \
	song-a-tiel-backend

heroku-run-docker:
	docker run -it -d \
	--name song-a-tiel-backend \
	-v `pwd`:/song-a-tiel \
	-w /song-a-tiel \
	-p 5000:5000 \
	-e SPOTIFY_CLIENT_ID -e SPOTIFY_CLIENT_SECRET \
	song-a-tiel-backend

exec-docker:
	docker exec -it song-a-tiel-backend bash

yeet-docker:
	docker stop song-a-tiel-backend
	docker rm song-a-tiel-backend

pip-install:
	pip install -r requirements.txt