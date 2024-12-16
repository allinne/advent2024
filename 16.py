#!/usr/bin/python3

# python3 -m doctest -v 16.py

'''
--- Day 16: Reindeer Maze ---

It's time again for the Reindeer Olympics! This year, the big event is the Reindeer Maze, where the Reindeer compete for the lowest score.

You and The Historians arrive to search for the Chief right as the event is about to start. It wouldn't hurt to watch a little, right?

The Reindeer start on the Start Tile (marked S) facing East and need to reach the End Tile (marked E). They can move forward one tile at a time (increasing their score by 1 point), but never into a wall (#). They can also rotate clockwise or counterclockwise 90 degrees at a time (increasing their score by 1000 points).

To figure out the best place to sit, you start by grabbing a map (your puzzle input) from a nearby kiosk. For example:

###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############
There are many paths through this maze, but taking any of the best paths would incur a score of only 7036. This can be achieved by taking a total of 36 steps forward and turning 90 degrees a total of 7 times:


###############
#.......#....E#
#.#.###.#.###^#
#.....#.#...#^#
#.###.#####.#^#
#.#.#.......#^#
#.#.#####.###^#
#..>>>>>>>>v#^#
###^#.#####v#^#
#>>^#.....#v#^#
#^#.#.###.#v#^#
#^....#...#v#^#
#^###.#.#.#v#^#
#S..#.....#>>^#
###############
Here's a second example:

#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################
In this maze, the best paths cost 11048 points; following one such path would look like this:

#################
#...#...#...#..E#
#.#.#.#.#.#.#.#^#
#.#.#.#...#...#^#
#.#.#.#.###.#.#^#
#>>v#.#.#.....#^#
#^#v#.#.#.#####^#
#^#v..#.#.#>>>>^#
#^#v#####.#^###.#
#^#v#..>>>>^#...#
#^#v###^#####.###
#^#v#>>^#.....#.#
#^#v#^#####.###.#
#^#v#^........#.#
#^#v#^#########.#
#S#>>^..........#
#################
Note that the path shown above includes one 90 degree turn as the very first move, rotating the Reindeer from facing East to facing North.

Analyze your map carefully. What is the lowest score a Reindeer could possibly get?
'''

import datetime, heapq, sys

def inp(fn):
    with open(fn, 'r') as f:
        lines = f.readlines()
    return [l.rstrip() for l in lines]

# f1 = inp('input/16-small.txt')
f1 = inp('input/16.txt')

def starting(field):
    for y in range(len(field)):
        for x in range(len(field[0])):
            if field[y][x] == 'S':
                return x, y
    sys.exit(3)

def price(field, x, y):
    # dir_ch = '^>v<'
    dxdy = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    visited = {(x,y)}
    q = [] # price, rest
    heapq.heappush(q, (0, (x, y, 1))) # initial dir = 1 >>>
    while len(q) > 0:
        price, rest = heapq.heappop(q) # curr candidate
        x, y, d = rest

        if field[y][x] == 'E':
            return price

        if field[y][x] != '#': # not (x, y) in visited and
            x1, y1 = x + dxdy[d][0], y + dxdy[d][1]
            if not (x1, y1) in visited and field[y1][x1] != '#':
                visited.add((x1, y1))
                heapq.heappush(q, (price + 1, (x1, y1, d)))

            dir2 = (d + 1) % 4
            x2, y2 = x + dxdy[dir2][0], y + dxdy[dir2][1]
            if not (x2, y2) in visited and field[y2][x2] != '#':
                heapq.heappush(q, (price + 1000, (x, y, dir2)))

            dir3 = d - 1
            if dir3 < 0: dir3 = 3
            x3, y3 = x + dxdy[dir3][0], y + dxdy[dir3][1]
            if not (x3, y3) in visited and field[y3][x3] != '#':
                heapq.heappush(q, (price + 1000, (x, y, dir3)))
    return 0

x, y = starting(f1)
p = price(f1, x, y)
print('===============================')
print('The answer: ', p)
print('===============================')
