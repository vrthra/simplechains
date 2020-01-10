#!/usr/bin/env python3
import urllib.parse as uparse
import sys
with open(sys.argv[1]) as f:
    while True:
        line = f.readline()
        if not line:
            break
        if line[-1] == '\n':
            print(repr(uparse.unquote(line[0:-1])))
        else:
            print(repr(uparse.unquote(line)))
