"""
Functions for interacting with the ChartLyrics API for getting lyrics

The album, artist to search lyrics for are REQUIRED query params to SearchLyric
The lyricId and lyricCheckSum are query params to GetLyric
"""

from difflib import get_close_matches
import requests

import xmltodict



LYRICS_BASE_URL = 'http://api.chartlyrics.com/apiv1.asmx/'


class Lyrics():
    def __init__(self):
        pass

    def get(self, song, artist):
        '''Get lyrics given song title and artist name'''

        assert(any([song, artist]))

        # format params
        params = {
            "song": song,
            "artist": artist
        }

        # do SearchLyric query. get list of songs
        searchResult = self._runQuery("SearchLyric", params)['ArrayOfSearchLyricResult']['SearchLyricResult']
        # trim off the lyricId = 0 ones
        # try:
        # print(searchResult)

        try:
            # [print(result) for result in searchResult if result.get('LyricId') not in ['0', None]]
            # dict of {song title: song json}. exclude lyricid=0 and anything that doesn't have lyricid
            validSongs = {result['Song']: result for result in searchResult if result.get('LyricId') not in ['0', None]}
            print(f'validSongs {validSongs}')
        except:
            print('No lyrics found.')
            return ''
        
        # if there are none left, return no lyrics
        if not validSongs:
            print('No songs with lyrics found.')
            return ''
        
        # figure out which ArrayOfSearchLyricResult.SearchLyricResult.Song most closely matches song
        titles = validSongs.keys()
        print(titles)
        match = get_close_matches(song, titles, n=1, cutoff=0)[0]
        print(match)
        # get lyricId and lyricCheckSum of that one
        matchSong = validSongs[match]
        lyricId, lyricCheckSum = matchSong['LyricId'], matchSong['LyricChecksum']
        print(lyricId, lyricCheckSum)

        ## ------------------------------
        # do GetLyric query
        # get GetLyricResult.Lyric


        
        return "lyrics"


    def _runQuery(self, path, params={}):

        response = requests.get(LYRICS_BASE_URL + path, params=params)
        # print(response.text)
        if response.status_code != 200:
            print('Page error.')
            return False
        # translate XML (gross) to JSON
        data = xmltodict.parse(response.text)
        print(data)

        return data