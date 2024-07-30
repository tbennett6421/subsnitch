#from __future__ import (print_function, unicode_literals, division, absolute_import)
__metaclass__ = type
__package_name__    = 'subsnitch'
__code_desc__       = 'burning subtitles/covers on audio tracks to produce video files'
__code_version__    = "v0.0.1"

import os
import argparse
import logging
from pprint import pprint as pp

def begin_logging():
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter(
            style="{",
            fmt="[{name}:{filename}] {levelname} - {message}"
        )
    )
    log = logging.getLogger(__package_name__)
    log.setLevel(logging.INFO)
    log.addHandler(handler)
    return log

def collect_args():
    parser = argparse.ArgumentParser(description=__code_desc__,
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-V', '--version', action='version', version=__code_version__)
    parser.add_argument('-v', '--verbose', action='count', default=0)
    args = parser.parse_args()
    return parser, args

def handle_args():
    # collect parser if needed to conditionally call usage: parser.print_help()
    parser, args = collect_args()
    return args

def main():
    log = begin_logging()
    args = handle_args()

    targets = []
    current_directory = os.getcwd()
    for filename in os.listdir(current_directory):
        if filename.endswith('.wav') or filename.endswith('.mp3'):
            base_name, extension = os.path.splitext(filename)
            print(f"Filename: {base_name}, Extension: {extension}")
            targets.append(filename)

    try:
        return 0
    except Exception as e:
        pp(e)
        raise e
    finally:
        pass

if __name__=="__main__":
    main()
