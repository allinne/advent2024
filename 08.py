#!/usr/bin/python3

# python3 -m doctest -v 08.py

'''
--- Day 8: Resonant Collinearity ---

You find yourselves on the roof of a top-secret Easter Bunny installation.

While The Historians do their thing, you take a look at the familiar huge antenna. Much to your surprise, it seems to have been reconfigured to emit a signal that makes people 0.1% more likely to buy Easter Bunny brand Imitation Mediocre Chocolate as a Christmas gift! Unthinkable!

Scanning across the city, you find that there are actually many such antennas. Each antenna is tuned to a specific frequency indicated by a single lowercase letter, uppercase letter, or digit. You create a map (your puzzle input) of these antennas. For example:

............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
The signal only applies its nefarious effect at specific antinodes based on the resonant frequencies of the antennas. In particular, an antinode occurs at any point that is perfectly in line with two antennas of the same frequency - but only when one of the antennas is twice as far away as the other. This means that for any pair of antennas with the same frequency, there are two antinodes, one on either side of them.

So, for these two antennas with frequency a, they create the two antinodes marked with #:

..........
...#......
..........
....a.....
..........
.....a....
..........
......#...
..........
..........
Adding a third antenna with the same frequency creates several more antinodes. It would ideally add four antinodes, but two are off the right side of the map, so instead it adds only two:

..........
...#......
#.........
....a.....
........a.
.....a....
..#.......
......#...
..........
..........
Antennas with different frequencies don't create antinodes; A and a count as different frequencies. However, antinodes can occur at locations that contain antennas. In this diagram, the lone antenna with frequency capital A creates no antinodes but has a lowercase-a-frequency antinode at its location:

..........
...#......
#.........
....a.....
........a.
.....a....
..#.......
......A...
..........
..........
The first example has antennas with two different frequencies, so the antinodes they create look like this, plus an antinode overlapping the topmost A-frequency antenna:

......#....#
...#....0...
....#0....#.
..#....0....
....0....#..
.#....A.....
...#........
#......#....
........A...
.........A..
..........#.
..........#.
Because the topmost A-frequency antenna overlaps with a 0-frequency antinode, there are 14 total unique locations that contain an antinode within the bounds of the map.

Calculate the impact of the signal. How many unique locations within the bounds of the map contain an antinode?
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
                dx = x2 - x1
                dy = y2 - y1
                ax1 = x1 - dx
                ay1 = y1 - dy
                if 0 <= ax1 < len(field[0]) and 0 <= ay1 < len(field):
                    # f[ay1][ax1] = True
                    antinodes.add( (ax1, ay1) )
                ax2 = x2 + dx
                ay2 = y2 + dy
                if 0 <= ax2 < len(field[0]) and 0 <= ay2 < len(field):
                    antinodes.add( (ax2, ay2) )
                    # f[ay2][ax2] = True

# for l in f:
#     print(''.join('#' if b else '.' for b in l))

print('===============================')
print('The answer: ', len(antinodes))
print('===============================')
