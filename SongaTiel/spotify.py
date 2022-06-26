"""
API wrapper for Spotify
"""

import os
import requests
import urllib.parse
from infotype import Type
from base64 import b64encode
import datetime


SPOTIFY_BASE_URL = 'https://api.spotify.com/v1/'
SPOTIFY_AUTH_URL = 'https://accounts.spotify.com/api/token'



class SpotifyWrapper():
    """API wrapper for Spotify API"""
    def __init__(self):
        pass


    def search(self, infoTypeRaw, song='', album='', artist=''):
        """
        SongaTiel uses this directly.
        Inputs: type, song, album, artist.
        - infotype is an instance of Type. example: Type.SONG
        Output: all info defined in the schema.
        """

        assert any([song, album, artist]), 'Must provide a song, album, or artist'
        assert isinstance(infoTypeRaw, Type), 'Info type is not an enumeration'

        # Determine filters
        filterArgs = {
            "track": song,
            "album": album,
            "artist": artist
        }
        if infoTypeRaw is Type.SONG:
            infoType = "track"  # Spotify calls a song a track
        elif infoTypeRaw is Type.ALBUM:
            filterArgs.pop('track', None)
            infoType = "album"  # Spotify calls a song a track
        elif infoTypeRaw is Type.ARTIST:
            filterArgs.pop('track', None)
            filterArgs.pop('album', None)
            infoType = "artist"  # Spotify calls a song a track
        else:
            # This should never happen
            infoType = str(infoTypeRaw.name.lower())

        # yeet empty arguments
        filters = { arg:filterArgs[arg] for arg in filterArgs if filterArgs[arg] }

        try:
            # get the item the user is looking for
            mainArg = filterArgs[infoType]
        except:
            print("Item to search for must not be empty.")
            raise ValueError

        # Format query string
        q = self._make_query_str(filters, mainArg)

        params = {
            "q": q,
            "type": infoType
        }

        # Hit the search endpoint. type=infoType, other params used in query string q
        searchJson = self._runQuery('search', params)

        # Pull out the Spotify ID
        try:
            spotify_id = searchJson[f'{infoType}s']['items'][0]['id']
        except:
            print('No results.')
            return {}
        
        # Hit the appropriate endpoint for the information type now that the ID is known
        infoJson = self._runQuery(f'{infoType}s/{spotify_id}')

        # Use infoType to clean up the JSON and prep for return to the user
        if infoType == "track":
            return self._track(infoJson)
        elif infoType == "album":
            return self._album(infoJson)
        else:
            return self._artist(infoJson)
    

    def _track(self, trackJson):
        """Return json info about a song (aka a track in Spotify terminology)"""
        name = trackJson['name']
        artist = trackJson['artists'][0]['name']
        release_date = trackJson['album']['release_date']
        album = trackJson['album']['name']
        length = str(datetime.timedelta(seconds=trackJson['duration_ms']/1000))
        length = length.split('.')[0]  # remove the extra milliseconds

        # Try to get related songs
        if trackJson.get('artists'):
            artistJson = trackJson.get('artists')

            # HACK: seed the genre as geek rock just to choose one
            # this is because most artists seem to not have genres returned here 
            # despite the spotify docs saying that they will return genres
            if not artistJson[0].get('genres'):
                artistJson[0]['genres'] = ['geek rock']
            
            if artistJson[0].get('id') and artistJson[0].get('genres'):
                artist_id, artist_genres = artistJson[0].get('id'), artistJson[0].get('genres')
                relatedJson = self._runQuery(f'recommendations',
                    params={
                        "seed_artists": artist_id,
                        "seed_genres": artist_genres[0],
                        "seed_tracks": trackJson['id']
                    }
                )
                related_songs = {track.get('name',''):[artist.get('name') for artist in track.get('artists',[]) if artist.get('name')]
                    for track in relatedJson['tracks']}
            else:
                related_songs = []
        else:
            related_songs = []

        return {
            "name": name or "",
            "artist": artist or "",
            "album": album or "",
            "release_date": release_date or "",
            "length": length or "",
            "related_songs": related_songs
        }
    

    def _album(self, albumJson):
        """Return json info about an album"""
        name = albumJson['name']
        artist = albumJson['artists'][0]['name']
        release_date = albumJson['release_date']
        tracklist = [track['name'] for track in albumJson['tracks']['items']]
        tracks_duration = [track['duration_ms'] for track in albumJson['tracks']['items']]
        album_duration = sum(tracks_duration) / 1000  # the track durations are in ms. convert to s
        length = str(datetime.timedelta(seconds=album_duration))
        length = length.split('.')[0]  # remove the extra milliseconds
        return {
            "name": name,
            "artist": artist,
            "tracklist": tracklist,
            "length": length,
            "release_date": release_date
        }

    
    def _artist(self, artistJson):
        """Return json info about an artist"""
        name = artistJson.get('name', '')
        genres = artistJson.get('genres', [])

        if artistJson.get('id'):
            # Get albums
            albumsJson = self._runQuery(f'artists/{artistJson.get("id")}/albums',
                params={
                    "limit": 50,
                    "include_groups": "album,compilation"
                }
            )
            # Extract albums and remove duplicates
            albums = list(set([album.get('name') for album in albumsJson.get('items',{})]))

            # Get related artists
            relatedJson = self._runQuery(f'artists/{artistJson.get("id")}/related-artists')
            related_artists = [artist.get('name','') for artist in relatedJson.get('artists',{})]
        else:
            albums = []
            related_artists = []
        
        return {
            "name": name,
            "albums": albums,
            "genres": genres,
            "related_artists": related_artists
        }


    def _runQuery(self, path, params={}):
        '''Helper function to actually do the query.
        Inputs:
            path: the path of the Spotify API
            params: any query params that might be present'''

        # HANDLE AUTH
        while True:
            try:
                token = self._handle_auth()
                break
            except:
                print("Problem with getting token, trying again")
                continue

        response = requests.get(SPOTIFY_BASE_URL + path, params=params, headers={'Authorization':f'Bearer {token}'})

        if not response.ok:
            print('Page error.')
            exit

        return response.json()


    def _handle_auth(self):
        """
        Handles Spotify API authentication.
        Uses the env vars to get a token
        """
        auth_str = f"{os.environ['SPOTIFY_CLIENT_ID']}:{os.environ['SPOTIFY_CLIENT_SECRET']}"
        auth_encoded = b64encode(auth_str.encode())
        response = requests.post(SPOTIFY_AUTH_URL,
            headers={
                "Authorization": "Basic " + auth_encoded.decode(),
                "Content-Type": "application/x-www-form-urlencoded"
            },
            data={
                "grant_type": "client_credentials"
            }
        )
        assert response.ok, "Could not get Spotify API token."

        return response.json()['access_token']


    def _make_query_str(self, filters={}, query=''):
        """
        Create a query string to put in the Spotify search
        Inputs:
        - filters: a dict of filters. 
        """
        search_str = query + ' '
        for filterType in filters:
            search_str += f'{filterType}:{filters[filterType]} '

        return search_str