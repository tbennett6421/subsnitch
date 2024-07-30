#from __future__ import (print_function, unicode_literals, division, absolute_import)
__metaclass__ = type
__package_name__    = 'subsnitch'
__code_desc__       = 'burning subtitles/covers on audio tracks to produce video files'
__code_version__    = "v0.0.1"

import os, sys
import argparse
import logging
from pprint import pprint as pp

class FileNotFoundError(Exception):
    """Custom exception to be raised when the file is not found."""
    pass

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

def explode(filename):
    base_name, extension = os.path.splitext(filename)
    return base_name, extension

def find_vtt_file(directory, filename, extension):
    """
    Searches the specified directory for a .vtt file that matches the
    filename or filename.ext.

    Raises:
        FileNotFoundError: If no matching .vtt file is found.
    """
    ## Sanity check. Prepend a dot to extension
    extension = '.' + extension.lstrip('.')

    vtt_filename = f"{filename}.vtt"
    vtt_with_ext_filename = f"{filename}{extension}.vtt"
    files_in_directory = os.listdir(directory)

    if vtt_filename in files_in_directory:
        return os.path.join(directory, vtt_filename)
    elif vtt_with_ext_filename in files_in_directory:
        return os.path.join(directory, vtt_with_ext_filename)
    else:
        raise FileNotFoundError(f"No matching .vtt file found for '{filename}' with extension '{extension}' in directory '{directory}'.")

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
