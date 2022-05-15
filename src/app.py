"""
Flask app
"""


from flask import Flask


app = Flask(__name__)

@app.route('/')
def info():
    return 'song-a-tiel! Wheeeee'



def main():
    # TODO: fill in
    pass


if __name__ == '__main__':
    main()
    app.run(debug=True, host='0.0.0.0')