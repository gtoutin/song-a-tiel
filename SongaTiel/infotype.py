"""
An enum info type
"""


from enum import Enum


class Type(Enum):
    SONG, ALBUM, ARTIST, ERROR = 1, 2, 3, 4