# subsnitch
subsnitch is a program I made for stitching coverart,audio,subtitles into a video format. Feel free to use this to add subtitles to any audio work or for translation purposes.

# Installation
I highly recommend you use `pipx` to install this, as it creates the virtualenv for you and seamlessly handles the loading of the virtual environment when running this tool. If you choose not to use `pipx`, you should create a virtualenv and possibly a wrapper script to launch this in the virtualenv.

```sh
pipx install subsnitch
```

# Usage

When executed without arguments, the program should scan the current working directory for [mp3, wav] files and then process them
    Look for {basename}.vtt, {basename}.{ext}.vtt                                                   assert failure
    Look for {basename}.[png,jpeg,jpg,webp], {basename}.{ext}.[png,jpeg,jpg,webp], cover.[png,jpeg,jpg]       assert failure
Alternatively the program may take arguments to alter how it functions

The following is the help for the program
```
usage: __main__.py [-h] [-V] [-v]

burning subtitles/covers on audio tracks to produce video files

options:
  -h, --help     show this help message and exit
  -V, --version  show program's version number and exit
  -v, --verbose
```

# Examples

```sh
No content
```

# Credits

This package was created with [Cookiecutter](https://github.com/cookiecutter/cookiecutter) and the [tbennett6421/pythoncookie](https://github.com/tbennett6421/pythoncookie) project template.
