#!/usr/bin/python3

# python3 -m doctest -v 04.py

'''
--- Day 4: Ceres Search ---

"Looks like the Chief's not here. Next!" One of The Historians pulls out a device and pushes the only button on it. After a brief flash, you recognize the interior of the Ceres monitoring station!

As the search for the Chief continues, a small Elf who lives on the station tugs on your shirt; she'd like to know if you could help her with her word search (your puzzle input). She only has to find one word: XMAS.

This word search allows words to be horizontal, vertical, diagonal, written backwards, or even overlapping other words. It's a little unusual, though, as you don't merely need to find one instance of XMAS - you need to find all of them. Here are a few ways XMAS might appear, where irrelevant characters have been replaced with .:

..X...
.SAMX.
.A..A.
XMAS.S
.X....
The actual word search will be full of letters instead. For example:

MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
In this word search, XMAS occurs a total of 18 times; here's the same word search again, but where letters not involved in any XMAS have been replaced with .:

....XXMAS.
.SAMXMS...
...S..A...
..A.A.MS.X
XMASAMX.MM
X.....XA.A
S.S.S.S.SS
.A.A.A.A.A
..M.M.M.MM
.X.X.XMASX
Take a look at the little Elf's word search. How many times does XMAS appear?

To begin, get your puzzle input.
'''

import sys

with open('input/04.txt', 'r') as f:
# with open('input/04-small.txt', 'r') as f:
    lines = f.readlines()
field = [l.rstrip() for l in lines]

xmas = 'XMAS'
id = 0
q = []
for y in range(len(field)): # put X
    for x in range(len(field[0])):
        if field[y][x] == xmas[id]:
            dir = 0
            points = [(x, y)]
            q.append( [dir, points] )
id += 1

# dir:
# 1 2 3
# 8 0 4
# 7 6 5

dxdy_to_dir = [
    [1, 2, 3],
    [8, 0, 4],
    [7, 6, 5]
]
dir_to_dxdy = [(0,0), (-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0)]
def dir_from_dxdy(dx, dy):
    '''
    >>> dir_from_dxdy(0, 0)
    0

    >>> dir_from_dxdy(-1, -1)
    1

    >>> dir_from_dxdy(1, 1)
    5

    >>> dir_to_dxdy[dir_from_dxdy(1, 1)]
    (1, 1)
    '''
    return dxdy_to_dir[dy + 1][dx + 1]

def is_valid(x, y):
    return True if 0 <= x < len(field[0]) and 0 <= y < len(field) else False

while id < len(xmas):
    new_q = []
    for dir, points in q:
        x, y = points[-1]
        if dir == 0: # first char at x,y; dir is unknown
            candidates = [(x-1, y-1), (x, y-1), (x+1, y-1),
                          (x-1, y),  (x+1, y),
                          (x-1, y+1), (x, y+1), (x+1, y+1)]
            valid = []
            for xc, yc in candidates:
                if is_valid(xc, yc):
                    valid.append( (xc, yc) )
            # any dir for second char
            continuation = [(x1, y1) for x1, y1 in valid if xmas[id] == field[y1][x1] ]

            for x1, y1 in continuation:
                dx = x1 - x
                dy = y1 - y
                new_dir = dir_from_dxdy(dx, dy)
                points = [(x, y), (x1, y1)]
                new_q.append([new_dir, points])
        else: # non-first char, dir is valid
            dx, dy = dir_to_dxdy[dir]
            new_x = x + dx
            new_y = y + dy
            if is_valid(new_x, new_y):
                if field[new_y][new_x] == xmas[id]:
                    points.append( (new_x, new_y) )
                    new_q.append([dir, points])
    q = new_q
    id += 1

print('===============================')
# print(q)
print('The answer: ', len(q))
print('===============================')
