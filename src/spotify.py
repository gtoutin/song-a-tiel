"""
Functions and stuff for wrangling spotify

intended use: 
SpotifyWrapper.
"""

import requests
from infotype import Type


SPOTIFY_BASE_URL = 'https://api.spotify.com/v1/'




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


    def search(self, infoType, song='', album='', artist=''):
        """
        SongaTiel uses this directly.
        Inputs: type, song, album, artist.
        - infotype is an instance of Type. example: Type.SONG
        Output: all necessary info.
        """

        assert any([song, album, artist]), 'Must provide a song, album, or artist'

        ## Format query string
        filterArgs = {
            "song": song,
            "album": album,
            "artist": artist
        }
        # yeet empty arguments
        filters = { arg:filterArgs[arg] for arg in filterArgs if filterArgs[arg] }
        try:
            # get the item the user is looking for
            mainArg = filterArgs[infoType.name.lower()]
        except:
            print("Item to search for must not be empty.")
            raise ValueError

        q = self._make_query_str(filters, mainArg)

        print(q)

        params = {
            "q": q,
            "type": infoType.name.lower()
        }

        # Hit the search endpoint. type=infoType, other params used in query string q

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

        response = requests.get(SPOTIFY_BASE_URL + path, params=params)

        if response.status_code != 200:
            print('Page error.')
            return False

        return response.json()


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
            search_str += f'{filterType}:{filters[filterType]}+'
        if search_str[-1] == '+':
            search_str = search_str[:-1]  # remove last +

        return search_str