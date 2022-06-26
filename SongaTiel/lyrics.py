"""
Wrapper for interacting with the ChartLyrics API for getting lyrics

Will return song lyrics given the artist and song for which to search lyrics
"""

from difflib import get_close_matches
import requests

import xmltodict



LYRICS_BASE_URL = 'http://api.chartlyrics.com/apiv1.asmx/'


class Lyrics():
    """
    ChartLyrics API Wrapper
    """
    def __init__(self):
        pass

    def get(self, song, artist):
        '''Get lyrics given song title and artist name'''

        assert any([song, artist]), 'Must provide both song and artist'

        # format params for SearchLyric
        params = {
            "song": song,
            "artist": artist
        }

        # do SearchLyric query. get list of songs
        searchResult = self._runQuery("SearchLyric", params).get('ArrayOfSearchLyricResult',{}).get('SearchLyricResult', [])

        try:
            # dict of {song title: song json}. exclude lyricid=0 and anything that doesn't have lyricid
            validSongs = {result['Song']: result for result in searchResult if result.get('LyricId') not in ['0', None]}
        except:
            print('No lyrics found.')
            return ''
        
        # if there are none left, return no lyrics
        if not validSongs:
            print('No songs with lyrics found.')
            return ''
        
        # figure out which ArrayOfSearchLyricResult.SearchLyricResult.Song most closely matches song
        titles = validSongs.keys()
        match = get_close_matches(song, titles, n=1, cutoff=0)[0]

        # get lyricId and lyricCheckSum of that one
        matchSong = validSongs[match]
        lyricId, lyricCheckSum = matchSong['LyricId'], matchSong['LyricChecksum']

        ## ------------------------------
        # set params for GetLyric query
        params = {
            "lyricId": lyricId,
            "lyricCheckSum": lyricCheckSum
        }

        try:
            # do GetLyric query and get the lyric
            lyrics = self._runQuery("GetLyric", params)['GetLyricResult']['Lyric']
        except:
            print('Lyrics for the song not found.')
            return ''

        return lyrics


    def _runQuery(self, path, params={}):
        '''Helper function to actually do the query.
        Inputs:
            path: the path of the ChartLyrics API
            params: any query params that might be present'''

        response = requests.get(LYRICS_BASE_URL + path, params=params)

        if response.status_code != 200:
            print('Page error.')
            return {}

        # translate XML (gross) to JSON
        data = xmltodict.parse(response.text)

        return data