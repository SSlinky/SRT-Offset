#!/usr/bin/python3

import re
import subtitle
import readerwriter
import argparse

from typing import List
from _version import __version__
import sys


def configure() -> argparse.Namespace:
    """Parses the arguments passed in by the cli"""
    parser = argparse.ArgumentParser(
        description=f'Subtitle Offsetter Version {__version__}')

    # Input file name
    parser.add_argument(
        'src_file',
        help='The input file name (must end with .srt)')

    # Offset seconds
    parser.add_argument(
        'offset', type=float,
        help='The offset value in seconds - supports decimal and negatives')

    # Overwrite file
    parser.add_argument(
        '-d', '--destination', required=False,
        help='The destination file name. If not provided overwrites old file.')

    parser.add_argument(
        '--version', action='version', version='%(prog)s '+__version__,
        help='show version information and quit')

    return parser.parse_args()


def offset(config: argparse.Namespace):
    """Offsets the subtitle file"""
    # Configuration
    src_file = config.src_file
    s_offset = config.offset
    dst_file = config.destination \
        if config.destination is not None else src_file

    print(dst_file)
    sys.exit(0)

    # Read the data from the text file
    data = readerwriter.io.read(src_file)

    # Parse to subtitle.Item and offset
    subs = load_subs(data)
    subs = offset_subs(subs, s_offset)

    # Write the data to text file
    readerwriter.Io.write(dst_file, outstring(subs))


def load_subs(data: List[str]) -> List[subtitle.Item]:
    """Loads the string data into subtitle.Item classes"""
    # Patterns
    IS_ID = r'^\d+$'
    IS_TS = r'^[0-9:,]{12} --> [0-9:,]{12}$'

    # Loop vars at function scope
    subs = []
    id = ''
    ts = ''
    tx = ''

    # Main parse loop
    for row in data:
        # Test if the data is an ID row
        if re.match(IS_ID, row):
            if '' not in (id, ts, tx):
                subs.append(subtitle.Item(id, ts, tx))
            id = row
            tx = ''
            continue

        # Test if the row is a timestamp
        if re.match(IS_TS, row):
            ts = row
            continue

        # Row must be subtitle text
        tx += row

    # Append the last subtitle
    if ' ' not in (id, ts, tx):
        subs.append(subtitle.Item(id, ts, tx))

    return subs


def offset_subs(subs: List[subtitle.Item],
                offset: float) -> List[subtitle.Item]:
    """Offsets the list of passed in subtitles"""
    return [sub.offset(offset) for sub in subs]


def outstring(subs: List[subtitle.Item]) -> str:
    """Converts a list of subtitle.Item into a string"""
    return ''.join([str(sub) for sub in subs])


if __name__ == '__main__':
    offset(configure())
