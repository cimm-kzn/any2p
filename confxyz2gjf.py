#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
#  Copyright 2014 stsouko <stsouko@live.ru>
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
__author__ = 'stsouko'
import sys


def main():
    if len(sys.argv) < 2:
        sys.exit('а файл угадать мне?')

    def numb():
        i = 0
        while True:
            i += 1
            yield i
    numb = numb()
    prevenerg = -10000
    solv = 0
    temp = 0
    reaction = (int(sys.argv[1].split('.')[1]) - 1) / 2
    if len(sys.argv) >= 3:
        temp = int(float(open(sys.argv[2]).readlines()[reaction].strip()) + 273)
    if len(sys.argv) == 4:
        solv = open(sys.argv[3]).readlines()[reaction].strip()

    for i in range(1, 10000):
        try:
            with open('%s.%04d.xyz' % (sys.argv[1], i)) as mol:
                inp = mol.readlines()
                if float(inp[1].strip().split(" ")[1]) - prevenerg > .001:
                    prevenerg = float(inp[1].strip().split(" ")[1])
                    inp.pop(0)
                    inp.append(' ')
                    if temp and solv:
                        inp[0] = "%%NProcShared=4\n# PM6 opt=(maxcycle=500) freq scrf(SMD,solvent=%s) temperature=%d\n\n conformer Energy %g\n\n0 1\n" % (solv, temp, prevenerg)
                    elif temp:
                        inp[0] = "%%NProcShared=4\n# PM6 opt=(maxcycle=500) freq temperature=%d\n\n conformer Energy %g\n\n0 1\n" % (temp, prevenerg)
                    elif solv:
                        inp[0] = "%%NProcShared=4\n# PM6 opt=(maxcycle=500) freq scrf(SMD,solvent=%s)\n\n conformer Energy %g\n\n0 1\n" % (solv, prevenerg)
                    else:
                        inp[0] = "%%NProcShared=4\n# PM6 opt=(maxcycle=500) freq\n\n conformer Energy %g\n\n0 1\n" % (prevenerg)
                    with open('%s.%04d.gjf' % (sys.argv[1], numb.next()), 'w') as out:
                        out.write(''.join(inp))
        except IOError:
            break

    return 0


if __name__ == '__main__':
    main()
