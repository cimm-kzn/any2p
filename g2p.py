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
#usage: script input_file o|s basis set
__author__ = 'stsouko'
import sys
import os
import re


def main():
    tasktype = {'o': dict(task="optimize", steps="200", scan=""),
                's': dict(task="scan", steps="50", scan=" fix=1,a,b,0,0\n value=2.3, 2.0\n points=16\n")}
    if len(sys.argv) < 2:
        sys.exit('а файл угадать мне?')
    if len(sys.argv) == 3:
        task = tasktype[sys.argv[2][0]]
    else:
        task = tasktype['o']

    task['basis'] = '/home/stsouko/.priroda/basis/3z'
    task['set'] = ''

    if len(sys.argv) > 3:
        task['basis'] = sys.argv[3]
        if len(sys.argv) == 5:
            task['set'] = '\n set=' + sys.argv[4]

    if not os.path.exists(sys.argv[1]):
        sys.exit('нихт файл' % sys.argv[1])

    mendel = dict(H=1, He=2, Li=3, Be=4, B=5, C=6, N=7, O=8, F=9, Ne=10, Na=11, Mg=12, Al=13, Si=14, P=15, S=16, Cl=17,
                  Ar=18, K=19, Ca=20, Sc=21, Ti=22, V=23, Cr=24, Mn=25, Fe=26, Co=27, Ni=28, Cu=29, Zn=30, Ga=31, Ge=32,
                  As=33, Se=34, Br=35, Kr=36, Rb=37, Sr=38, Y=39, Zr=40, Nb=41, Mo=42, Tc=43, Ru=44, Rh=45, Pd=46,
                  Ag=47, Cd=48, In=49, Sn=50, Sb=51, Te=52, I=53, Xe=54, Cs=55, Ba=56, La=57, Ce=58, Pr=59, Nd=60,
                  Pm=61, Sm=62, Eu=63, Gd=64, Tb=65, Dy=66, Ho=67, Er=68, Tm=69, Yb=70, Lu=71, Hf=72, Ta=73, W=74,
                  Re=75, Os=76, Ir=77, Pt=78, Au=79, Hg=80, Tl=81, Pb=82, Bi=83, Po=84, At=85, Rn=86, Fr=87, Ra=88,
                  Ac=89, Th=90, Pa=91, U=92, Np=93, Pu=94, Am=95, Cm=96, Bk=97)

    lines = open(sys.argv[1]).readlines()
    for line in lines:
        data = re.search('\s*-?[0-9]+\s+[0-9]+', line)
        if data:
            data = data.group().split(' ')
            task['charge'] = data[0].strip()
            task['mult'] = data[1].strip()
            break

    print "$system memory=2000 disk=10 path=/tmp $end\n" \
          "$control\n" \
          " task=%(task)s\n" \
          " theory=DFT\n four=1\n" \
          " basis=%(basis)s\n" \
          "$end\n"\
          "$dft functional=PBE $end\n" \
          "$optimize\n" \
          " steps=%(steps)s\n" \
          "%(scan)s$end\n" \
          "$molecule\n" \
          " charge=%(charge)s\n" \
          " mult=%(mult)s\n" \
          " cartesian" \
          "%(set)s" % task

    for line in lines:
        cord = re.search('[A-Z][a-z]?(\s+-?[0-9]+\.[0-9]+){3}', line)
        if cord:
            print "%3s" % str(mendel[cord.group()[:2].strip()]) + "%50s" % cord.group()[2:].strip()
    print "$end"
    return 0


if __name__ == '__main__':
    main()

