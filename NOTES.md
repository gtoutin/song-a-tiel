

## Roadmap
- [ ] Figure out which endpoints will give the info needed and update the endpoints list with that info
- [X] Set up the docker container
- [ ] Makefile
- [ ] Set up the Flask app


## Endpoints
- [ ] /artist/{name}/similar
- [ ] /artist/{name}/info
- [ ] /song/{name}/similar
- [ ] /song/{name}/info
- [ ] /song/{name}/lyrics

for each endpoint will need the spotify id, so the spotify search needs to be used before each one to get the id

## Spotify endpoints
- GET https://api.spotify.com/v1/search
    - query params
        - q a string to search for things
            - filters
                - album, artist, track, year, upc, tag:hipster, tag:new, isrc, and genre
                    - tag:hipster can be used to return only albums with the lowest 10% popularity.
        - type
            - comma separated list of "album""artist""playlist""track""show""episode"
- GET /tracks/{id}
    - track length in ms
    - explicit
    - popularity
    - 30s preview
    - album
        - href a link to the spotify endpoint with more album details
        - image links
        - id and name of album with that song
        - album info
    - artists
        - href a link to the spotify endpoint with more album details
        - uri for artist

        

## API powered by Flask
- Compatible with a frontend
- Dockerized

## Abandon hope for future plans...
- Expose the Flask API to the internet somehow
    - Replit?
- Maybe the user can run a website locally and that website is a client to the server on replit
- Include album images
- Bandcamp?
- Merch?
