#!/usr/bin/env python3
# coding: utf-8

# wrapper for Python JSON parser

COMPLETE = 0
INCOMPLETE = 1
WRONG = 2

import json
def validate(input_str):
    """ return:
        rv: "complete", "incomplete" or "wrong", 
        n: the index of the character -1 if not applicable
        c: the character where error happened  "" if not applicable

        The n and c are extra information that is useful but not strictly
        needed.
    """
    try:
        json.loads(input_str)
        return "complete",-1,""
    except Exception as e:
        msg = str(e)
        if msg.startswith("Expecting"):
            # Expecting value: line 1 column 4 (char 3)
            n = int(msg.rstrip(')').split()[-1])
            # If the error is "outside" the string, it can still be valid
            if n >= len(input_str):
                return "incomplete", n, ""
            else:
                return "wrong", n, input_str[n]
        elif msg.startswith("Unterminated"):
            # Unterminated string starting at: line 1 column 1 (char 0)
            n = int(msg.rstrip(')').split()[-1])
            if n >= len(input_str):
                return "incomplete", n, ""
            else:
                return "incomplete",n, input_str[n]
        elif msg.startswith("Extra data"):
            n = int(msg.rstrip(')').split()[-1])
            if n >= len(input_str):
                return "wrong", n, ""
            else:
                return "wrong",n, input_str[n]
        elif msg.startswith("Invalid "):
            idx = msg.find('(char ')
            eidx = msg.find(')')
            s = msg[idx+6:eidx]
            n = int(s)
            return "wrong",n, input_str[n]
        else:
            raise e

import sys
def main(fn):
    with open(fn) as f:
        inp = f.read()
        rv, n, c = validate(inp)
        if rv == 'complete':
            sys.exit(COMPLETE)
        elif rv == 'incomplete':
            sys.exit(INCOMPLETE)
        elif rv == 'wrong':
            sys.exit(WRONG)
        else:
            assert False

if __name__ == '__main__':
    main(sys.argv[1])
