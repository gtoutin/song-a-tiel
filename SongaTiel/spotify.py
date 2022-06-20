"""
Functions and stuff for wrangling spotify

intended use: 
SpotifyWrapper.
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
    def __init__(self):
        pass


    def search(self, infoTypeRaw, song='', album='', artist=''):
        """
        SongaTiel uses this directly.
        Inputs: type, song, album, artist.
        - infotype is an instance of Type. example: Type.SONG
        Output: all necessary info.
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
        # print('FILTERS!!!!')
        # print(filters)
        try:
            # get the item the user is looking for
            mainArg = filterArgs[infoType]
        except:
            print("Item to search for must not be empty.")
            raise ValueError

        # Format query string
        q = self._make_query_str(filters, mainArg)
        # print(q)

        params = {
            "q": q,
            "type": infoType
        }
        # print(params)
        # return
        # Hit the search endpoint. type=infoType, other params used in query string q
        searchJson = self._runQuery('search', params)
        # print(searchJson)

        # Pull out the Spotify ID
        try:
            spotify_id = searchJson[f'{infoType}s']['items'][0]['id']
            # print(spotify_id)
        except:
            print('No results.')
            return {}
        
        # Hit the appropriate endpoint for the information type now that the ID is known
        infoJson = self._runQuery(f'{infoType}s/{spotify_id}')
        # print(infoJson)

        # Use infoType to clean up the JSON and prep for return to the user
        if infoType == "track":
            # print(self._track(infoJson))
            return self._track(infoJson)
        elif infoType == "album":
            # print(self._album(infoJson))
            return self._album(infoJson)
        else:
            # print(self._artist(infoJson))
            return self._artist(infoJson)
    

    def _track(self, trackJson):
        name = trackJson['name']
        artist = trackJson['artists'][0]['name']
        album = trackJson['album']['name']
        length = str(datetime.timedelta(seconds=trackJson['duration_ms']/1000))
        return {
            "name": name or "",
            "artist": artist or "",
            "album": album or "",
            "year": "",
            "length": length or "",
            "related_songs":""
        }
    

    def _album(self, albumJson):
        name = albumJson['name']
        artist = albumJson['artists'][0]['name']
        date_released = albumJson['release_date']
        tracklist = [track['name'] for track in albumJson['tracks']['items']]
        tracks_duration = [track['duration_ms'] for track in albumJson['tracks']['items']]
        album_duration = sum(tracks_duration) / 1000  # the track durations are in ms. convert to s
        return {
            "name": name,
            "artist": artist,
            "tracklist": tracklist,
            "length": str(datetime.timedelta(seconds=album_duration)),
            "date_released": date_released
        }

    
    def _artist(self, artistJson):
        name = artistJson.get('name')
        if artistJson.get('id'):
            print('HIT artist/albums')
            albumsJson = self._runQuery(f'artists/{artistJson.get("id")}/albums',
                params={
                    "limit": 50,
                    "include_groups": "album,compilation"
                }
            )
            # Extract albums and remove duplicates
            albums = list(set([album.get('name') for album in albumsJson['items']]))
        else:
            albums = []
        print({
            "name": name,
            "albums": albums,
            "info": "",
            "related_artists": ""
        })
        return {
            "name": name,
            "albums": albums,
            "info": "",
            "related_artists": ""
        }


    def _runQuery(self, path, params={}):
        '''Helper function to actually do the query.
        Inputs:
            path: the path of the Spotify API
            params: any query params that might be present'''

        # HANDLE AUTH
        token = self._handle_auth()
        print(token)

        response = requests.get(SPOTIFY_BASE_URL + path, params=params, headers={'Authorization':f'Bearer {token}'})
        print(response.json())

        if not response.ok:
            print('Page error.')
            exit

        print(response.url)
        return response.json()


    def _handle_auth(self):
        """
        Handles Spotify API authorization.
        Uses the env vars to get a token
        """
        auth_str = f"{os.environ['SPOTIFY_CLIENT_ID']}:{os.environ['SPOTIFY_CLIENT_SECRET']}"
        auth_encoded = b64encode(auth_str.encode())
        # print(auth_str)
        # print(auth_encoded)
        # print(auth_encoded.decode())
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