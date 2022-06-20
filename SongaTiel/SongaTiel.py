"""
Overall wrapper for getting info about stuff.
User-facing.

Usage:
- init an object
- pass any of album, song, artist to the search method
"""

from infotype import Type
from spotify import SpotifyWrapper
from lyrics import Lyrics

class SongaTiel():
    def __init__(self):
        pass

    def search(self, song='', album='', artist=''):
        '''Searches for a song, album, and/or artist'''

        ## Follow the rules to determine which function to use
        if song:  # song + anything = song
            # use other specified things if they are there
            resultData = self._song(song, album=album, artist=artist)
        # album and artist, return info about album
        else:
            if album:  # no song + album = album
                resultData = self._album(album, song=song, artist=artist)
            else:  # artist on its own
                resultData = self._artist(artist, song=song, album=album)

        return resultData

    
    def _song(self, song, album='', artist=''):
        # Get info from Spotify
        sp = SpotifyWrapper()
        songInfo = sp.search(Type.SONG, song, album, artist)

        # Only get lyrics if Spotify actually found a song
        # Otherwise the lyrics are probably wrong
        if songInfo:
            # Get lyrics
            ly = Lyrics()
            lyrics = ly.get(song, artist)
        else:
            lyrics = ""

        return {
            "type": Type.SONG.name,
            "data": {
                "name": songInfo.get('name',''),
                "artist": songInfo.get('artist',''),
                "album": songInfo.get('album',''),
                "release_date": songInfo.get('release_date',''),
                "lyrics": lyrics,
                "length": songInfo.get('length',''),
                "related_songs": songInfo.get('related_songs',[])
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