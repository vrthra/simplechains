#!/usr/bin/env python3
# coding: utf-8
# import pudb
# bp = pudb.set_trace

import json
import urllib.parse as uparse
import string
import random
import subprocess


COMPLETE = 0
INCOMPLETE = 1
WRONG = 2

TIMEOUT = 10

class O:
    def __init__(self, **keys): self.__dict__.update(keys)
    def __repr__(self): return str(self.__dict__)

def init_log(prefix, var, module):
    with open('%s.log' % module, 'a+') as f:
        print(prefix, ':==============',var, file=f)

def do(command, env=None, shell=False, log=False, **args):
    result = subprocess.Popen(command,
        stdout = subprocess.PIPE,
        stderr = subprocess.STDOUT,
    )
    stdout, stderr = result.communicate(timeout=TIMEOUT)
    if log:
        with open('do.log', 'a+') as f:
            print(json.dumps({'cmd':command, 'env':env, 'exitcode':result.returncode}), env, file=f)
    return O(returncode=result.returncode, stdout=stdout, stderr=stderr)

def get_next_char(log_level):
    set_of_chars = string.printable # ['[',']','{','}','(',')','<','>','1','0','a','b',':','"',',','.', '\'']
    idx = random.randrange (0,len(set_of_chars),1)
    input_char = set_of_chars[idx]
    return input_char

def validate(cmd, fname):
    res = do([cmd, fname])
    return res.returncode

def generate(cmd, log_level):
    """
    Feed it one character at a time, and see if the parser rejects it. 
    If it does not, then append one more character and continue. 
    If it rejects, replace with another character in the set. 
    :returns completed string
    """
    prev_str = ""
    while True:
        char = get_next_char(log_level)
        curr_str = prev_str + str(char)
        with open('cur_str.json_', 'w+') as f:
            f.write(curr_str)
        rv = validate(cmd, 'cur_str.json_')
        if rv == COMPLETE:
            return curr_str
        elif rv == INCOMPLETE:
            prev_str = curr_str
            continue
        elif rv == WRONG: # try again with a new random character do not save current character
            continue
        else:
            print("ERROR What is this I dont know !!!")
            break
    return None

def create_valid_strings(cmd, n, log_level):
    i = 0
    while True:
        created_string = generate(cmd, log_level)
        if created_string is not None:
            print(repr(created_string))
            with open('%s.log' % cmd, 'a+') as f:
                print(uparse.quote(created_string), file=f)
            i = i +1
            if (i >= n):
                break

def main(cmd):
    create_valid_strings(cmd, 100000, 0)

import sys
if __name__ == '__main__':
    main(sys.argv[1])
