"""
An enum info type to organize all possible response types
"""


from enum import Enum


class Type(Enum):
    """Enumeration type to organize the 4 different response types:
    SONG, ALBUM, ARTIST, ERROR"""
    SONG, ALBUM, ARTIST, ERROR = 1, 2, 3, 4