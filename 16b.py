#!/usr/bin/python3

# python3 -m doctest -v 16.py

'''
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

Your puzzle answer was 107512.

The first half of this puzzle is complete! It provides one gold star: *

--- Part Two ---

Now that you know what the best paths look like, you can figure out the best spot to sit.

Every non-wall tile (S, ., or E) is equipped with places to sit along the edges of the tile. While determining which of these tiles would be the best spot to sit depends on a whole bunch of factors (how comfortable the seats are, how far away the bathrooms are, whether there's a pillar blocking your view, etc.), the most important factor is whether the tile is on one of the best paths through the maze. If you sit somewhere else, you'd miss all the action!

So, you'll need to determine which tiles are part of any best path through the maze, including the S and E tiles.

In the first example, there are 45 tiles (marked O) that are part of at least one of the various best paths through the maze:

###############
#.......#....O#
#.#.###.#.###O#
#.....#.#...#O#
#.###.#####.#O#
#.#.#.......#O#
#.#.#####.###O#
#..OOOOOOOOO#O#
###O#O#####O#O#
#OOO#O....#O#O#
#O#O#O###.#O#O#
#OOOOO#...#O#O#
#O###.#.#.#O#O#
#O..#.....#OOO#
###############
In the second example, there are 64 tiles that are part of at least one of the best paths:

#################
#...#...#...#..O#
#.#.#.#.#.#.#.#O#
#.#.#.#...#...#O#
#.#.#.#.###.#.#O#
#OOO#.#.#.....#O#
#O#O#.#.#.#####O#
#O#O..#.#.#OOOOO#
#O#O#####.#O###O#
#O#O#..OOOOO#OOO#
#O#O###O#####O###
#O#O#OOO#..OOO#.#
#O#O#O#####O###.#
#O#O#OOOOOOO..#.#
#O#O#O#########.#
#O#OOO..........#
#################
Analyze your map further. How many tiles are part of at least one of the best paths through the maze?
'''

import datetime, heapq, sys

def inp(fn):
    with open(fn, 'r') as f:
        lines = f.readlines()
    return [l.rstrip() for l in lines]

# f1 = inp('input/16-small-01.txt')
# f1 = inp('input/16-small-02.txt')
f1 = inp('input/16-small.txt')
# f1 = inp('input/16.txt')

def starting(field):
    for y in range(len(field)):
        for x in range(len(field[0])):
            if field[y][x] == 'S':
                return x, y
    sys.exit(3)

def price(field, x, y):
    # dir_ch = '^>v<'
    dxdy = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    visited = {(x, y, 1): 0}
    q = [] # price, rest
    heapq.heappush(q, (0, (x, y, 1, [(x, y)]))) # initial dir = 1 >>>
    best = 1000000000
    all = set()
    while len(q) > 0:
        price, rest = heapq.heappop(q) # curr candidate
        x, y, d, path = rest

        if field[y][x] == 'E':
            if price <= best:
                best = price
                # print('path', path)
                for xy in path:
                    all.add(xy)

        if field[y][x] != '#': # not (x, y) in visited and
            x1, y1 = x + dxdy[d][0], y + dxdy[d][1]
            price1 = price + 1
            if price1 <= best and field[y1][x1] != '#':
                if not (x1, y1, d) in visited or price1 <= visited[(x1, y1, d)]:
                    visited[(x1, y1, d)] = price1
                    path1 = path[:]
                    path1.append((x1, y1,))
                    heapq.heappush(q, (price1, (x1, y1, d, path1)))

            dir2 = (d + 1) % 4
            x2, y2 = x + dxdy[dir2][0], y + dxdy[dir2][1]
            price2 = price + 1000
            if field[y2][x2] != '#' and price2 <= best:
                if not (x2, y2, dir2) in visited or price2 <= visited[(x2, y2, dir2)]:
                    path2 = path[:]
                    heapq.heappush(q, (price2, (x, y, dir2, path2)))

            dir3 = d - 1
            if dir3 < 0: dir3 = 3
            x3, y3 = x + dxdy[dir3][0], y + dxdy[dir3][1]
            price3 = price + 1000
            if field[y3][x3] != '#' and price3 <= best:
                if not (x3, y3, dir3) in visited or price3 <= visited[(x3, y3, dir3)]:
                    path3 = path[:]
                    heapq.heappush(q, (price3, (x, y, dir3, path3)))

    # field = [[ch for ch in s] for s in field]
    # for x, y in all:
    #     field[y][x] = 'O'
    # for s in field:
    #     print([''.join(s)])
    # print(f'best={best}')
    return len(all)

x, y = starting(f1)
p = price(f1, x, y)
print('===============================')
print('The answer: ', p)
print('===============================')
