"""
Functions and stuff for wrangling spotify

intended use: 
SpotifyWrapper.
"""

import requests

SPOTIFY_BASE_URL = ''




def get_id(q):
    """
    Query Spotify API for the ID you need to interact with other endpoints
    Input: q, a query string for the search
    """
    # TODO: fill in
    pass


def query_str(filters=[], query=''):
    """
    Create a query string to put in the Spotify search
    Inputs:
    - filters: a list of filters. 
      possible ones are 
      album, artist, track, year, upc, tag:hipster, tag:new, isrc, and genre
    """
    search_str = ','.join(filters) + ' ' + query
    return search_str




class SpotifyWrapper():
    def __init__():
        pass

    def request(endpoint, base_url=SPOTIFY_BASE_URL):
        pass


    def search(q='', types=['album','artist','track']):
        """
        Hits the search endpoint
        Inputs:
        - q: a search string ready to put into the API
        - types: a list of types of item to search for.
        possible ones are
        album, artist, playlist, track, show, episode

        """
        pass