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

        # No results check
        if not resultData['data'].get('name'):
            resultData['type'] = Type.ERROR.name

        return resultData

    
    def _song(self, song, album='', artist=''):
        # Get info from Spotify
        sp = SpotifyWrapper()
        songInfo = sp.search(Type.SONG, song, album, artist)

        # For reuse in lyrics search
        song_name = songInfo.get('name','')
        artist_name = songInfo.get('artist','')

        # Only get lyrics if Spotify actually found a song
        # Otherwise the lyrics are probably wrong
        if songInfo:
            # Get lyrics
            ly = Lyrics()
            # Use more accurate spotify names
            lyrics = ly.get(song_name, artist_name)
        else:
            lyrics = ""

        return {
            "type": Type.SONG.name,
            "data": {
                "name": song_name,
                "artist": artist_name,
                "album": songInfo.get('album',''),
                "release_date": songInfo.get('release_date',''),
                "lyrics": lyrics,
                "length": songInfo.get('length',''),
                "related_songs": songInfo.get('related_songs',[])
            }
        }


    def _album(self, album, song='', artist=''):
        # Get info from Spotify
        sp = SpotifyWrapper()
        albumInfo = sp.search(Type.ALBUM, song, album, artist)

        return {
            "type": Type.ALBUM.name,
            "data": {
                "name": albumInfo.get('name',''),
                "artist": albumInfo.get('artist',''),
                "tracklist": albumInfo.get('tracklist',[]),
                "length": albumInfo.get('length',''),
                "release_date": albumInfo.get('release_date','')
            }
        }


    def _artist(self, artist, song='', album=''):
        # Get info from Spotify
        sp = SpotifyWrapper()
        artistInfo = sp.search(Type.ARTIST, song, album, artist)

        return {
            "type": Type.ARTIST.name,
            "data": {
                "name": artistInfo.get('name',''),
                "albums": artistInfo.get('albums',[]),
                "genres": artistInfo.get('genres',[]),
                "related_artists": artistInfo.get('related_artists',[])
            }
        }