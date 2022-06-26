"""
Main SongATiel module for the CLI version
"""

import argparse
from SongaTiel import SongaTiel


def main():
    """
    Parse and validate CLI args. Use the args in a SongATiel search
    """
    # handle args
    arg_parser = argparse.ArgumentParser(
        prog='SongaTiel',
        description='Search for a song, album, or artist',
        add_help=True
    )
    arg_parser.add_argument('--song')
    arg_parser.add_argument('--album')
    arg_parser.add_argument('--artist')

    args = arg_parser.parse_args()

    # essential check
    assert any([args.song, args.album, args.artist]), 'Must provide a song, album, or artist'

    # start the search
    st = SongaTiel()
    print(st.search(song=args.song, album=args.album, artist=args.artist))


if __name__ == '__main__':
    main()