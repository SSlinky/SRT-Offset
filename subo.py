import re
import os
import sys
import shutil
import argparse

from io import FileIO
from datetime import datetime, timedelta

from _version import __version__

def parse_options() -> argparse.Namespace:
    """Parses the arguments passed in by the cli"""
    # Create the parser and set displayed message when the -h or --help is passed in
    parser = argparse.ArgumentParser(description = 'Offset srt subtitles.')
    # The input file name
    parser.add_argument('srt', type=FileIO, help='The input file name (must end with .srt)')
    # The offset value in seconds
    parser.add_argument('offset', type=float, help='The offset value in seconds - supports decimal and negatives')
    # Overwrite option - true if present
    parser.add_argument('-o', '--overwrite', action='store_true', default=False, help='overwite original file')
    # Version information
    parser.add_argument('--version', action='version', version='%(prog)s '+__version__, help='show version information and quit')

    return parser.parse_args()


def offset_time_seconds(t: datetime, s: float) -> datetime:
    """Returns a time that is t offset by s seconds"""
    return t + timedelta(seconds=s)

def parse_time(t: str) -> datetime:
    """Parses a datetime from srt format"""
    return datetime.strptime('00010101' + t, r'%Y%m%d%H:%M:%S,%f')

def format_time(t: datetime) -> str:
    """Returns a datetime in srt format"""
    return datetime.strftime(t, r'%H:%M:%S,%f')[:-3]

def srt_offset(t: str) -> str:
    """Wrapper for the functions that parse, offset, and format a time stamp"""
    global OFFSET
     


def offset_subtitles(options: argparse.Namespace):
    """Modify the input srt time stamps"""
    global OFFSET
    OFFSET = options.offset

    # Check the type of the passed in file
    if options.srt.name[:-4] != '.srt':
        sys.exit('ERROR: Invalid srt file')
    # Get the input file name
    inf = options.srt.name
    # Generate the output file name from the old file name
    outf = inf if options.overwite else os.path.splitext(inf)[0] + 'resync.srt'
    # Define the regexp
    exp = r'^(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})$'
    """00:03:21,360 --> 00:03:22,964"""

    # Read and modify the srt
    with open(inf, 'w', encoding = 'utf-8') as f:
        lines = f.readlines()
        matches = [re.match(exp, line) for line in lines]

        srt = [
            # The original line if no timestamp match exists
            l if m is None
            # The offset timestamps
            else f'{srt_offset(m.group(1))} --> {srt_offset(m.group(2))}'
            for l,m in zip(lines,matches) 
        ]


if __name__ == "__main__":
    offset_subtitles(parse_options())




def modify_file(options):
    if '.srt' not in options.srt_file.name:
        sys.exit("ERROR: invalid srt file")

    out_filename = os.path.splitext(options.srt_file.name)[0] + '-resync.srt'
    with open(out_filename, 'w', encoding = 'utf-8') as out:
        with open(options.srt_file.name, 'r', encoding = 'utf-8') as srt:
            for line in srt.readlines():
                match = re.search(r'^(\d+:\d+:\d+,\d+)\s+--\>\s+(\d+:\d+:\d+,\d+)', line)
                if match:
                    pass
                    # out.write("%s --> %s\n" % (
                    #     offset_time(options.offset, match.group(1)),
                    #     offset_time(options.offset, match.group(2))
                    #     ))
                else:
                    out.write(line)

    if options.overwrite:
        shutil.move(out_filename, options.srt_file.name)
