#!/usr/bin/python3

# python3 -m doctest -v 08b.py

'''
--- Part Two ---

Watching over your shoulder as you work, one of The Historians asks if you took the effects of resonant harmonics into your calculations.

Whoops!

After updating your model, it turns out that an antinode occurs at any grid position exactly in line with at least two antennas of the same frequency, regardless of distance. This means that some of the new antinodes will occur at the position of each antenna (unless that antenna is the only one of its frequency).

So, these three T-frequency antennas now create many antinodes:

T....#....
...T......
.T....#...
.........#
..#.......
..........
...#......
..........
....#.....
..........
In fact, the three T-frequency antennas are all exactly in line with two antennas, so they are all also antinodes! This brings the total number of antinodes in the above example to 9.

The original example now has 34 antinodes, including the antinodes that appear on every antenna:

##....#....#
.#.#....0...
..#.#0....#.
..##...0....
....0....#..
.#...#A....#
...#..#.....
#....#.#....
..#.....A...
....#....A..
.#........#.
...#......##
Calculate the impact of the signal using this updated model. How many unique locations within the bounds of the map contain an antinode?
'''

import sys
from collections import defaultdict

with open('input/08.txt', 'r') as f:
# with open('input/08-small.txt', 'r') as f:
    lines = f.readlines()
field = [l.rstrip() for l in lines]

antenas = defaultdict(list)
for y in range(len(field)):
    for x in range(len(field[0])):
        ch = field[y][x]
        if ch != '.':
            antenas[ch].append((x, y))

antinodes = set()
# f = [[False for x in range(len(field[0]))] for y in range(len(field))]
for ch, xy in antenas.items():
    if len(xy) > 1:
        for id1 in range(len(xy) - 1):
            for id2 in range(id1 + 1, len(xy)):
                x1, y1 = xy[id1]
                x2, y2 = xy[id2]
                if x1 > x2: # make x1 always left-most: swap if needed
                    x1, y1, x2, y2 = x2, y2, x1, y1
                antinodes.add( (x1, y1) )
                antinodes.add( (x2, y2) )
                dx = x2 - x1
                dy = y2 - y1
                ax1 = x1 - dx
                ay1 = y1 - dy
                while 0 <= ax1 < len(field[0]) and 0 <= ay1 < len(field):
                    # f[ay1][ax1] = True
                    antinodes.add( (ax1, ay1) )
                    ax1 -= dx
                    ay1 -= dy
                ax2 = x2 + dx
                ay2 = y2 + dy
                while 0 <= ax2 < len(field[0]) and 0 <= ay2 < len(field):
                    antinodes.add( (ax2, ay2) )
                    # f[ay2][ax2] = True
                    ax2 += dx
                    ay2 += dy

# for l in f:
#     print(''.join('#' if b else '.' for b in l))

print('===============================')
print('The answer: ', len(antinodes))
print('===============================')
