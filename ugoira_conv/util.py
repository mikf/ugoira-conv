# -*- coding: utf-8 -*-

# Copyright 2015 Mike Fährmann
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

import os

def silentremove(filename):
    """Silently remove a file"""
    try:
        os.remove(filename)
    except OSError:
        pass

class DurationDict():
    """Provides a mapping between animation frames and their duration"""

    def __init__(self, durationfile, default=100):
        self._dict = None
        self._default = default
        try:
            ddict = {}
            with open(durationfile) as dfile:
                for line in dfile:
                    name, duration = line.split()
                    ddict[name] = int(duration)
            self._dict = ddict
        except (IOError, KeyError):
            pass

    def __getitem__(self, key):
        try:
            return self._dict[key]
        except (TypeError, KeyError):
            return self._default
