# -*- coding: utf-8 -*-

# Copyright 2015 Mike Fährmann
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

__author__     = "Mike Fährmann"
__copyright__  = "Copyright 2015 Mike Fährmann"

__license__    = "GPLv2"
__version__    = "0.1"
__maintainer__ = "Mike Fährmann"
__email__      = "mike_faehrmann@web.de"

import argparse
from . import ugoira

def parse_cmdline_options():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "ugoira",
        metavar="UGOIRA"
    )
    parser.add_argument(
        "-f", "--format",
        metavar="FMT", default="webm", choices=ugoira.UgoiraConverter.formats,
        help="target format"
    )
    parser.add_argument(
        "-t", "--target-directory",
        metavar="DIR", default=None,
        help="target direcotry for converted file"
    )
    parser.add_argument(
        "-n", "--filename",
        metavar="N", default=None,
        help="filename for converted file"
    )
    parser.add_argument(
        "-d", "--durationfile",
        metavar="DF", default=None,
        help="textfile to specify durations for each frame"
    )
    return parser.parse_args()

def main():
    args = parse_cmdline_options()
    uconv = ugoira.UgoiraConverter(args.ugoira, args.durationfile)
    try:
        uconv.convert(
            fmt=args.format,
            path=args.target_directory,
            filename=args.filename
        )
    except KeyboardInterrupt:
        print("\nKeyboardInterrupt")
