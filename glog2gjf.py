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

    pul = []
    solv = 0
    temp = 0
    out = []
    for l in open(sys.argv[1]):
        if 'Solvent              :' in l and not solv:
            solv = l.split(',')[0].split(':')[1].strip()
        if ' Temperature ' in l:
            temp = int(float(l.replace('   ', ' ').replace('  ', ' ').strip().split(' ')[1]))

        if 'Redundant internal coordinates taken from checkpoint file' in l:
            pul.append(l)
        elif pul and 'Recover connectivity data from disk' not in l:
            pul.append(l)
        elif 'Recover connectivity data from disk' in l and pul:
            pul[0] = "%NProcShared=4\n"
            cm = pul[2].strip().replace("  ", " ").split(' ')
            pul[2] = "%s %s\n" % (cm[2], cm[5])
            pul.append(' ')
            out = pul
            pul = None
    print temp, solv
    out[1] = "# PM6 opt=(maxcycle=500) freq scrf(SMD,solvent=%s) temperature=%d\n\n (c) stsouko\n\n" % (solv, temp)
    with open('%s.gjf' % sys.argv[1][:-4], 'w') as f:
        f.write(''.join(out))

    return 0


if __name__ == '__main__':
    main()