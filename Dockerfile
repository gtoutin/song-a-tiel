FROM python:3.9.5

RUN mkdir /song-a-tiel
WORKDIR /song-a-tiel
COPY . /song-a-tiel

RUN pip install -r requirements.txt

ENTRYPOINT python SongaTiel/app.py