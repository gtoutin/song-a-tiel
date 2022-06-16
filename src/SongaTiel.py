"""
Overall wrapper for getting info about stuff.
User-facing.

Usage:
- init an object
- pass any of album, song, artist to the search method
"""

from enum import Enum


class Type(Enum):
    SONG, ALBUM, ARTIST = 1, 2, 3

class SongaTiel():
    def __init__(self):
        pass

    def search(self, song='', album='', artist=''):
        '''Searches for a song, album, and/or artist'''

        ## Follow the rules to determine which function to use
        if song:  # song + anything = song
            # use other specified things if they are there
            resultData = self.song(song, album=album, artist=artist)
        # album and artist, return info about album
        else:
            if album:  # no song + album = album
                resultData = self._album(album, song=song, artist=artist)
            else:  # artist on its own
                resultData = self._artist(artist, song=song, album=album)

        return resultData

    
    def _song(self, song, album='', artist=''):
        return {
            "type": Type.SONG.name,
            "data": {
                "artist": "",
                "album": "",
                "year": 0000,
                "lyrics": "",
                "length": "",
                "related_songs": []
            }
        }


    def _album(self, album, song='', artist=''):
        return {
            "type": Type.ALBUM.name,
            "data": {
                "artist": "",
                "tracklist": "",
                "length": "",
                "date_released": "YYYY-MM-DD"
            }
        }


    def _artist(self, artist, song='', album=''):
        return {
            "type": Type.ARTIST.name,
            "data": {
                "albums": [],
                "info": "",
                "related_artists": []
            }
        }