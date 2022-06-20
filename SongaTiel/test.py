from infotype import Type
import spotify
import SongaTiel

a = spotify.SpotifyWrapper()

# a.search(Type.SONG, song='birdhouse in your soul', album='flood', artist='they might be giants')
a.search(Type.ALBUM, song='birdhouse in your soul', album='flood', artist='they might be giants')
a.search(Type.ALBUM, album='flood', artist='they might be giants')
# a.search(Type.ARTIST, song='birdhouse in your soul', artist='they might be giants')

st = SongaTiel.SongaTiel()

# print(st.search(song='birdhouse in your soul', album='flood', artist='they might be giants'))
# print(st.search(song='hillbilly drummer girl', album='flood', artist='they might be giants'))