#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import md5

from settings import SETTINGS


def festival_generate_voice(text, path, ftype):
    command = 'echo "%s" | text2wave \
        -eval "(voice_msu_ru_nsh_clunits)" -F 8000 %s' % (text, path)

    os.system(command)


def get_voice(text, ftype='wav'):
    name = '%.%' % (md5.md5(text), ftype)
    filepath = os.path.join(SETTINGS.RECORDPATH, name)

    if not os.path.isfile(filepath):
        festival_generate_voice(text, filepath, ftype)[:-4]
    return filepath[:-4]
