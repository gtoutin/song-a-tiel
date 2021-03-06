"""
Flask app for the web app version of SongATiel
"""

import os

from flask import Flask, request, Response, render_template

from SongaTiel import SongaTiel
from infotype import Type


app = Flask(__name__)   # Flask app
st = SongaTiel()        # SongaTiel object


@app.route('/', methods=['GET'])
def homepage():
    """Serve the homepage"""
    return render_template('index.html')


@app.route('/results/')
def results():
    """Serve a results page. Could be song, album, artist, or the No Results page"""
    # Grab the query params from the request.args dict
    song, album, artist = request.args.get("song",""), request.args.get("album",""), request.args.get("artist","")

    # Run the search
    st_results = st.search(song=song, album=album, artist=artist)
    st_data = st_results['data']

    if st_results['type'] == Type.SONG.name:
        print('Serving song page')
        return render_template('song.html',
            song=st_data['name'],
            artist=st_data['artist'],
            album=st_data['album'],
            release_date=st_data['release_date'],
            lyrics=st_data['lyrics'],
            length=st_data['length'],
            related_songs=st_data['related_songs'],
        )
    elif st_results['type'] == Type.ALBUM.name:
        print('Serving album page')
        return render_template('album.html',
            album=st_data['name'],
            artist=st_data['artist'],
            release_date=st_data['release_date'],
            length=st_data['length'],
            tracklist=st_data['tracklist'],
            art_link=st_data['album_art'],
        )
    elif st_results['type'] == Type.ARTIST.name:
        print('Serving artist page')
        return render_template('artist.html',
            artist=st_data['name'],
            albums=st_data['albums'],
            genres=st_data['genres'],
            rel_artists=st_data['related_artists'],
        )
    elif st_results['type'] == Type.ERROR.name:
        print('Serving error page')
        return render_template('no_results.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))