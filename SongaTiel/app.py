"""
Flask app
"""


from flask import Flask, request, Response, render_template
import json

from SongaTiel import SongaTiel
from infotype import Type


app = Flask(__name__)   # Flask app
st = SongaTiel()        # SongaTiel object


@app.route('/', methods=['GET'])
def homepage():
    return render_template('index.html')


@app.route('/results/')
def info():
    # Grab the query params from the request.args dict
    song, album, artist = request.args.get("song",""), request.args.get("album",""), request.args.get("artist","")

    # Run the search
    st_results = st.search(song=song, album=album, artist=artist)
    st_data = st_results['data']
    
    # # Make and return the search results
    # resp = Response(json.dumps(st_results))
    # resp.content_type = "application/json"

    if st_results['type'] == Type.SONG.name:
        return render_template('song.html',
            song=st_data['name'],
            artist=st_data['artist'],
            album=st_data['album'],
            release_date=st_data['release_date'],
            lyrics=st_data['lyrics'],
            length=st_data['length'],
        )



def main():
    # TODO: fill in
    pass


if __name__ == '__main__':
    main()
    app.run(debug=True, host='0.0.0.0')