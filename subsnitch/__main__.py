#from __future__ import (print_function, unicode_literals, division, absolute_import)
__metaclass__ = type
__package_name__    = 'subsnitch'
__code_desc__       = 'burning subtitles/covers on audio tracks to produce video files'
__code_version__    = "v0.0.1"

import os, sys
import argparse
import logging
from pprint import pprint as pp

## Third Party libraries
import ffmpeg
from moviepy.editor import ImageClip, AudioFileClip

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

def pathjoin(directory, filename):
    return os.path.join(directory, filename)

def explode(filename):
    base_name, extension = os.path.splitext(filename)
    return base_name, extension

def find_x_file(directory, filename, extension, needle, raisable=True):
    """
    Searches the specified directory for an abritrary extension that matches the
    filename or filename.ext.

    Raises:
        FileNotFoundError: If no matching .needle file is found.
    """
    ## Sanity check. Prepend a dot to extension
    extension = '.' + extension.lstrip('.')
    needle = '.' + needle.lstrip('.')

    needle_filename = f"{filename}{needle}"
    needle_with_ext_filename = f"{filename}{extension}{needle}"
    files_in_directory = os.listdir(directory)

    if needle_filename in files_in_directory:
        return pathjoin(directory, needle_filename)
    elif needle_with_ext_filename in files_in_directory:
        return pathjoin(directory, needle_with_ext_filename)
    else:
        if raisable:
            raise FileNotFoundError(f"No matching .vtt file found for '{filename}' with extension '{extension}' in directory '{directory}'.")
        else:
            return None

def find_vtt_file(directory, filename, extension):
    return find_x_file(directory, filename, extension, ".vtt")

def find_image_file(directory, filename, extension):
    # Search for images matching the targeted audio file
    acceptable_extensions = ['.png', '.jpg', '.jpeg', '.webp']
    for needle in acceptable_extensions:
        rval = find_x_file(directory, filename, extension, needle, raisable=False)
        if rval is not None:
            return rval

    # If not found, look for a fallback file named 'cover'
    for ext in acceptable_extensions:
        cover_filename = f'cover{ext}'
        cover_path = pathjoin(directory, cover_filename)
        # Check if the cover file exists
        if os.path.isfile(cover_path):
            return cover_path

    # If neither is found, return None
    # Images are optional
    return None

def make_selections(directory):
    targets = []
    for filename in os.listdir(directory):
        if filename.endswith('.wav') or filename.endswith('.mp3'):
            # Audio Selection
            audiofile = pathjoin(directory, filename)
            base_name, extension = explode(filename)
            # Subtitle Selection
            subtitles = find_vtt_file(directory, base_name, extension)
            imagefile = find_image_file(directory, base_name, extension)
            target = {
                "audio": audiofile,
                "vtt": subtitles,
                "img": imagefile,
            }
            targets.append(target)
    return targets

def create_subtitled_video(image=None, audio=None, vtt=None, output=None):
    # Validate arguments
    assert None not in [audio, vtt]
    if output == None:
        filename, extension = explode(audio)
        basefile = os.path.basename(filename) + ".mp4"
        output = filename + ".mp4"

    print("[*] Creating subtitled video")
    print("[*] Audio: %s" % audio)
    print("[*]   Img: %s" % image)
    print("[*]   VTT: %s" % vtt)
    print("[*] Video: %s" % output)
    print("[*] VideoFile: %s" % basefile)

    # Load the audio/images
    audio_clip = AudioFileClip(audio)
    duration = audio_clip.duration
    image_clip = ImageClip(image, duration=duration)

    # Set the audio to the image clip
    video_clip = image_clip.set_audio(audio_clip)

    # Save the video without subtitles first
    temp_video_path = "temp_video.mp4"
    video_clip.write_videofile(temp_video_path, codec="libx264", fps=24)

    # Use ffmpeg to add the subtitles
    ffmpeg.input(temp_video_path).output(output, vf=f"subtitles={vtt}", format='mp4').run(overwrite_output=True)
    os.remove(temp_video_path)

def main():
    log = begin_logging()
    args = handle_args()
    targets = make_selections(os.getcwd())
    for target in targets:
        create_subtitled_video(image=target['img'], audio=target['audio'], vtt=target['vtt'])
        print(f"[**] Audio:{target['audio']}")
        print(f"[**]   VTT:{target['vtt']}")
        print(f"[**]   IMG:{target['img']}")

    try:
        return 0
    except Exception as e:
        pp(e)
        raise e
    finally:
        pass

if __name__=="__main__":
    main()
