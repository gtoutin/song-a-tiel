### SongaTiel module

import argparse
import SongaTiel


def main():
    st = SongaTiel.SongaTiel()
    print(st.search(song='birdhouse in your soul', album='flood', artist='they might be giants'))


if __name__ == '__main__':
    main()