# song-a-tiel
Lookup songs and bands and discover new ones

## Installation and Setup
This project runs in docker.

- `make build-docker`
- `make run-docker`

At this point, the website is up and running on localhost:5000.
`make exec-docker` is available to get a shell inside the container if you wish to run the CLI.

### CLI version
- `make exec-docker`
- `python SongaTiel/__main__.py --song <songname> --album <albumname> --artist <artistname>`

See test cases below for examples.

## SCHEMAS
Note the `"type"` in the returned JSON. If the returned data is in an error state, `"type"` will be `ERROR` instead of whichever info type was requested.
### song
```JSON
{
    "type": "SONG",
    "data": {
        "name": "",
        "artist": "",
        "album": "",
        "release_date": "",
        "lyrics": "",
        "length": "",
        "related_songs": {
            "<song title>": ["<artist name>", ...],
        }
    }
}
```
### album
```JSON
{
    "type": "ALBUM",
    "data": {
        "name": "",
        "artist": "",
        "tracklist": [],
        "length": "",
        "release_date": "",
        "album_art": ""
    }
}
```
### artist
```JSON
{
    "type": "ARTIST",
    "data": {
        "name": "",
        "albums": [],
        "genres": [],
        "related_artists": []
    }
}
```

## FUTURE WORK
- [ ] Fix length (duration) formatting
- [X] Implement error responses. aka say no results instead of regular format w empty strings
    - [X] Related: cleanly handle errors. I have assertion errors for now
- [ ] Make module runnable. aka `python3 -m SongaTiel --whatever-args` or better yet `./SongaTiel --whatever`
- [ ] More docs are always good. Say exactly what could be empty in the schema and what is required
- [ ] Don't return lyrics for the wrong song. Try "When He Died" by Lemon Demon.

## TEST CASES
### song + artist = song
`python3 SongaTiel/__main__.py --song "american music" --artist "violent femmes"`
### song + album = song
`python3 SongaTiel/__main__.py --song "what do i get" --album "singles going steady"`
### album + artist = album
`python3 SongaTiel/__main__.py --album "are we not men?" --artist devo`
### things on their own
`python3 SongaTiel/__main__.py --song birdhouse`

`python3 SongaTiel/__main__.py --album weezer`

`python3 SongaTiel/__main__.py --artist "they might be giants"`
### all 3 at once
#### good
`python3 SongaTiel/__main__.py --song waiting --album "return of the rentals" --artist rentals`
#### bad
`python3 SongaTiel/__main__.py --song birdhouse --album weezer --artist "ok go"`

