#!/usr/bin/python3

import re
import subtitle
import readerwriter


FILENAME = 'tests/data/example{}.srt'
FILENAME = 'tests/data/Game.of.Thrones.S07E06.720p.WEB.h264-TBS{}.srt'
OFFSET = 4.203

IS_ID = r'^\d+$'
IS_TS = r'^[0-9:,]{12} --> [0-9:,]{12}$'

data = readerwriter.io.read(FILENAME.format(''))
subs = []

id = ''
ts = ''
tx = ''

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


outstr = ''

for sub in subs:
    sub.offset(OFFSET)
    outstr += str(sub)

readerwriter.io.write(FILENAME.format('_1'), outstr)
