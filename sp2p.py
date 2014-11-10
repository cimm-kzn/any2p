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
#
__author__ = 'stsouko'
import sys
import os


def main():
    if len(sys.argv) < 2:
        sys.exit('а файл угадать мне?')
    if not os.path.exists(sys.argv[1]):
        sys.exit('нихт файл' % sys.argv[1])

    print "$system memory=2000 disk=10 path=/tmp $end\n" \
          "$control\n" \
          " task=hessian\n" \
          " theory=DFT\n" \
          " four=1\n" \
          " basis=/home/stsouko/.priroda/basis/basis4.in\n" \
          "$end\n" \
          "$dft functional=PBE $end\n" \
          "$optimize\n" \
          " steps=100\n" \
          " saddle=1\n" \
          "$end"
    bestfit = -999999.
    for line in open(sys.argv[1]):
        if line[:5] == 'SCAN>':
            if line[:7] == 'SCAN> n':
                energy = float(line.split(',')[-1].strip()[2:])
                if energy > bestfit:
                    bestfit = energy
                    mol =[]
                    updmark = True
                else:
                    updmark = False
            elif updmark:
                mol += [line[5:].rstrip()]
    for line in mol:
        print line
    return 0


if __name__ == '__main__':
    main()
