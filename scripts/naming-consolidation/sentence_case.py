#!/usr/bin/python3

import os
from re import search, fullmatch
import sys
import tempfile
import subprocess

LINE_PATTERN = '^=+ [^A-Z]*[A-Z].*[A-Z].*$'
WORD_PATTERN = '[A-Z][a-z-]*'
SKIPPED = ['Git', 'Red', 'Hat', 'Jolokia', 'Agroal', 'Developer', 'Studio', 'Nodeshift']

def convert(string):
    first = True
    converted = []
    for token in string.split():
        if fullmatch(WORD_PATTERN, token) and not first and not token in SKIPPED:
            converted.append(token.lower())
        else:
            converted.append(token)
        if search('[^=]', token):
            first = False
    return ' '.join(converted) + '\n'


def analyze_file(filename):
    temp_filename = tempfile.mkstemp()[1]
    with open(temp_filename, 'w') as tf:
        with open(filename, 'r') as f:
            for l in f.readlines():
                match = search(LINE_PATTERN, l)
                if match:
                    tf.write(convert(l))
                else:
                    tf.write(l)
    subprocess.check_call(['cp', temp_filename, os.path.realpath(filename)])
    os.unlink(temp_filename)


if __name__ == '__main__':
    for f in sys.argv[1:]:
        analyze_file(f)

