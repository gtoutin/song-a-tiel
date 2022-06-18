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


SPOTIFY_BASE_URL = 'https://api.spotify.com/v1/'
SPOTIFY_AUTH_URL = 'https://accounts.spotify.com/api/token'



def _get_id(q):
    """
    Query Spotify API for the ID you need to interact with other endpoints
    Input: q, a query string for the search
    """
    # TODO: fill in
    pass



class SpotifyWrapper():
    def __init__(self):
        pass

    def request(self, endpoint, base_url=SPOTIFY_BASE_URL):
        pass


    def search(self, infoTypeRaw, song='', album='', artist=''):
        """
        SongaTiel uses this directly.
        Inputs: type, song, album, artist.
        - infotype is an instance of Type. example: Type.SONG
        Output: all necessary info.
        """

        assert any([song, album, artist]), 'Must provide a song, album, or artist'

        if infoTypeRaw is Type.SONG:
            infoType = "track"
        else:
            infoType = infoTypeRaw.name.lower()

        ## Format query string
        filterArgs = {
            "track": song,  # Spotify calls a song a track
            "album": album,
            "artist": artist
        }
        # yeet empty arguments
        filters = { arg:filterArgs[arg] for arg in filterArgs if filterArgs[arg] }
        try:
            # get the item the user is looking for
            mainArg = filterArgs[infoType]
        except:
            print("Item to search for must not be empty.")
            raise ValueError

        q = self._make_query_str(filters, mainArg)

        # print(q)

        params = {
            "q": q,
            "type": infoType,
        }

        # Hit the search endpoint. type=infoType, other params used in query string q
        searchJson = self._runQuery('search', params)
        print(searchJson)

        # Use infoType to determine which endpoint to hit after searching for id


    def _run_search(self, q='', types=['album','artist','track']):
        """
        Hits the search endpoint.
        Inputs:
        - q: a search string ready to put into the API
        - types: a list of types of item to search for.
        possible ones are
        album, artist, playlist, track, show, episode

        """
        pass


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
            return False

        print(response.url)
        return response.json()


    def _handle_auth(self):
        """Handles Spotify API authorization.
        Uses the env vars to get a token already encoded in b64"""
        auth_str = f"{os.environ['SPOTIFY_CLIENT_ID']}:{os.environ['SPOTIFY_CLIENT_SECRET']}"
        auth_encoded = b64encode(auth_str.encode())
        # print(auth_str)
        # print(auth_encoded)
        print(auth_encoded.decode())
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
        - filters: a list of filters. 
        possible ones are 
        album, artist, track, year, upc, tag:hipster, tag:new, isrc, and genre
        """

        search_str = query + ' '
        for filterType in filters:
            search_str += f'{filterType}:{filters[filterType]} '

        print()
        print(search_str)
        print(urllib.parse.quote_plus(search_str))

        return search_str