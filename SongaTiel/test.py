"""
This file contains tests. To run the tests, uncomment the tests you want and run this file.
"""

from infotype import Type
import spotify
import SongaTiel


## SPOTIFY WRAPPER TESTS

a = spotify.SpotifyWrapper()

# print(a.search(Type.SONG, song='birdhouse in your soul', album='flood', artist='they might be giants'))
# print(a.search(Type.SONG, song='hello', artist='adele'))
# print(a.search(Type.ALBUM, song='birdhouse in your soul', album='flood', artist='they might be giants'))
# print(a.search(Type.ALBUM, album='flood', artist='they might be giants'))

# print(a.search(Type.ARTIST, song='birdhouse in your soul', artist='they might be giants'))
# print(a.search(Type.ARTIST, song='birdhouse in your soul', album='flood', artist='they might be giants'))
# print(a.search(Type.ARTIST, album='flood', artist='they might be giants'))
# print(a.search(Type.ARTIST, artist='they might be giants'))

# assert a.search(Type.ARTIST, song='birdhouse in your soul', album='flood', artist='they might be giants') is not None
# assert a.search(Type.ARTIST, album='flood', artist='they might be giants') is not None
# assert a.search(Type.ARTIST, artist='they might be giants') is not None



## SONGATIEL TESTS

st = SongaTiel.SongaTiel()

# SONG TESTS
# print(st.search(song='birdhouse in your soul', album='flood', artist='they might be giants'))
# print(st.search(song='hillbilly drummer girl', album='flood', artist='they might be giants'))

# ALBUM TESTS
# print(st.search(album='flood', artist='they might be giants'))
# print(st.search(album='weezer', artist='they might be giants'))

# ARTIST TESTS
# print(st.search(artist='they might be giants'))
# print(st.search(artist='asdfjhlajerthwailuhofuyaholwuehflaohlefaulwief'))