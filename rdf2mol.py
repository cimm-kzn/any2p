#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
#  Copyright 2013 stsouko <stsouko@live.ru>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#usage: script input file o/s
import os

__author__ = 'stsouko'
import sys


def main():
    if len(sys.argv) < 2:
        sys.exit('а файл угадать мне?')
    if not os.path.exists(sys.argv[1]):
        sys.exit('нихт файл' % sys.argv[1])

    def numb():
        i = 0
        while True:
            i += 1
            yield i
    numb = numb()
    pul = []
    for l in open(sys.argv[1]):
        if '$MOL' in l:
            pul.append(l)
        elif pul and 'M  END' not in l:
            pul.append(l)
        elif 'M  END' in l and pul:
            pul.append(l)

            with open('mol.%05d' % numb.next()+'.mol', 'w') as f:
                f.write(''.join(pul[1:]))
            pul = []

    return 0


if __name__ == '__main__':
    main()