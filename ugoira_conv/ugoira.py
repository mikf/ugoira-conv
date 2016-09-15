# -*- coding: utf-8 -*-

# Copyright 2015 Mike Fährmann
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

import os.path
import shutil
import zipfile
import subprocess
import tempfile
from . import util

class UgoiraConverter():
    """Convert ugoira (pixiv-animations) to several other formats"""

    formats = ["webm", "gif", "gifpalette"]

    def __init__(self, zfile=None, durationfile=None):
        self._zipfile = zfile
        self._imgdir = None
        if zfile is None:
            pass # TODO: load from url
        if durationfile is None:
            durationfile = os.path.splitext(zfile)[0] + ".txt"
        self._ddict = util.DurationDict(durationfile)

    def __del__(self):
        """Remove temporary directory"""
        try:
            shutil.rmtree(self._imgdir)
        except TypeError:
            pass

    def convert(self, fmt="webm", path=None, filename=None):
        """Convert ugoira to given format"""
        if fmt not in self.formats:
            raise Exception("format not supported")
        if path is None:
            path = os.path.dirname(self._zipfile)
        if filename is None:
            filename = os.path.splitext(
                os.path.basename(self._zipfile))[0]
        target = os.path.join(path, filename)
        getattr(self, "_convert_" + fmt)(target)

    def _convert_gif(self, path):
        """Convert ugoira to animated gif"""
        self._call(
            ["ffmpeg", "-protocol_whitelist", "file,pipe", "-safe", "0",
             "-i", "-", "-an", "-y", path + ".gif"])

    def _convert_gifpalette(self, path):
        """Convert ugoira to animated gif while using a palette"""
        palette = "palette.png"
        try:
            self._call(
                ["ffmpeg", "-protocol_whitelist", "file,pipe", "-safe", "0",
                 "-i", "-", "-an", "-vf", "palettegen", "-y", palette])
            self._call(
                ["ffmpeg", "-protocol_whitelist", "file,pipe", "-safe", "0",
                 "-i", "-", "-i", palette, "-an",
                 "-filter_complex", "paletteuse", "-y", path + ".gif"])
        finally:
            util.silentremove(palette)

    def _convert_webm(self, path):
        """Convert ugoira to webm"""
        cmd = ["ffmpeg", "-protocol_whitelist", "file,pipe", "-safe", "0",
               "-i", "-", "-an", "-c:v", "libvpx", "-quality", "best",
               "-qmin", "0", "-qmax", "20", "-bufsize", "1000k", "-crf", "4",
               "-f", "webm", "-pass"]
        try:
            self._call(cmd + ["1", "-y", "/dev/null"])
            self._call(cmd + ["2", "-y", path + ".webm"])
        finally:
            util.silentremove("ffmpeg2pass-0.log")

    def _extract(self):
        """Extract images in zipfile to temporary directory"""
        if self._imgdir is None:
            self._imgdir = tempfile.mkdtemp()
            zipfile.ZipFile(self._zipfile).extractall(path=self._imgdir)
        return self._imgdir

    def _ffconcat(self, duration=1):
        """Generator to list all files in ffconcat-format"""
        drtn = 0
        imgdir = self._extract()
        yield b"ffconcat version 1.0\n"
        while drtn < duration:
            for file in sorted(os.listdir(imgdir)):
                fduration = self._ddict[file]
                drtn += fduration
                path = os.path.join(imgdir, file)
                yield "".join(("file ", path, "\n")).encode()
                yield "".join(("duration ", str(fduration/1000), "\n")).encode()

    def _call(self, cmd):
        """Execute external programm and feed the output of the _ffconcat()-
        generator into its standard-input"""
        with subprocess.Popen(cmd, stdin=subprocess.PIPE) as proc:
            for line in self._ffconcat():
                proc.stdin.write(line)
