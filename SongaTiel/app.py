"""
Flask app
"""


from flask import Flask, request, Response
from SongaTiel import SongaTiel
import json


app = Flask(__name__)   # Flask app
st = SongaTiel()        # SongaTiel object

@app.route('/')
def info():
    # Grab the query params from the request.args dict
    song, album, artist = request.args.get("song",""), request.args.get("album",""), request.args.get("artist","")

    # Run the search
    st_results = st.search(song=song, album=album, artist=artist)
    
    # Make and return the search results
    resp = Response(json.dumps(st_results))
    resp.content_type = "application/json"
    return resp



def main():
    # TODO: fill in
    pass


if __name__ == '__main__':
    main()
    app.run(debug=True, host='0.0.0.0')