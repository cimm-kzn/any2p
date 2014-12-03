#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
# Copyright 2013,2014 stsouko <stsouko@live.ru>
#
# This program is free software; you can redistribute it and/or modify
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
import sys
import os


def main():
    if len(sys.argv) < 2:
        sys.exit('а файл угадать мне?')
    if not os.path.exists(sys.argv[1]):
        sys.exit('нихт файл: %s' % sys.argv[1])

    bestfit = -9999999.
    mol = []
    task = dict(memory=1000, disk=5, path='/tmp', basis='/home/stsouko/.priroda/basis/3z', func='PBE', four='0',
                grid='1.0e-08', iter='16,16', conv='1.0e-06, 1.0e-03')
    for line in open(sys.argv[1]):
        if ' Memory: ' in line:
            task['memory'] = line[9:].split(' ')[0].strip('gmkt')
        if ' Disk: ' in line:
            task['disk'] = line[9:].split(' ')[0].strip('gmkt')
            task['path'] = line.strip().split(' ')[-1][1:-1]
        if 'Theoretical Method' in line:
            task['theory'] = line.strip().split(' ')[-1]
        if 'Basis set input:' in line:
            task['basis'] = line.strip().split(' ')[-1][1:-1]
        if 'Approximation to' in line:
            task['func'] = line.strip().split(' ')[-1]
        if 'scalar-relativistic' in line:
            task['four'] = 1
        if ' grid: accuracy=' in line:
            task['grid'] = line[16:].split(',')[0]
        if ' scf options:' in line:
            task['iter'] = line[14:].strip().split(';')[1].split('=')[1]
            task['conv'] = line[14:].split(';')[0].split('=')[1]

        if line[:5] == 'SCAN>':
            if line[:7] == 'SCAN> n':
                energy = float(line.split(',')[-1].strip()[2:])
                if energy > bestfit:
                    bestfit = energy
                    mol = ['En= %.5f' % energy]
                    updmark = True
                else:
                    updmark = False
            elif updmark:
                mol += [line[5:].rstrip()]
    print "$system memory=%(memory)s disk=%(disk)s path=%(path)s $end\n" \
          "$control\n" \
          " task=hessian\n" \
          " theory=%(theory)s\n" \
          " four=%(four)s\n" \
          " basis=%(basis)s\n" \
          "$end\n" \
          "$dft functional=%(func)s $end\n" \
          "$grid accuracy=%(grid)s $end\n" \
          "$scf\n convergence=%(conv)s\n iterations=%(iter)s\n $end\n" \
          "$optimize\n" \
          " steps=100\n" \
          " saddle=1\n" \
          "$end" % task

    for line in mol:
        print line
    return 0


if __name__ == '__main__':
    main()
