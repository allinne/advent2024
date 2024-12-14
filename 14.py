#!/usr/bin/python3

# python3 -m doctest -v 14.py

'''
--- Day 14: Restroom Redoubt ---

One of The Historians needs to use the bathroom; fortunately, you know there's a bathroom near an unvisited location on their list, and so you're all quickly teleported directly to the lobby of Easter Bunny Headquarters.

Unfortunately, EBHQ seems to have "improved" bathroom security again after your last visit. The area outside the bathroom is swarming with robots!

To get The Historian safely to the bathroom, you'll need a way to predict where the robots will be in the future. Fortunately, they all seem to be moving on the tile floor in predictable straight lines.

You make a list (your puzzle input) of all of the robots' current positions (p) and velocities (v), one robot per line. For example:

p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
Each robot's position is given as p=x,y where x represents the number of tiles the robot is from the left wall and y represents the number of tiles from the top wall (when viewed from above). So, a position of p=0,0 means the robot is all the way in the top-left corner.

Each robot's velocity is given as v=x,y where x and y are given in tiles per second. Positive x means the robot is moving to the right, and positive y means the robot is moving down. So, a velocity of v=1,-2 means that each second, the robot moves 1 tile to the right and 2 tiles up.

The robots outside the actual bathroom are in a space which is 101 tiles wide and 103 tiles tall (when viewed from above). However, in this example, the robots are in a space which is only 11 tiles wide and 7 tiles tall.

The robots are good at navigating over/under each other (due to a combination of springs, extendable legs, and quadcopters), so they can share the same tile and don't interact with each other. Visually, the number of robots on each tile in this example looks like this:

1.12.......
...........
...........
......11.11
1.1........
.........1.
.......1...
These robots have a unique feature for maximum bathroom security: they can teleport. When a robot would run into an edge of the space they're in, they instead teleport to the other side, effectively wrapping around the edges. Here is what robot p=2,4 v=2,-3 does for the first few seconds:

Initial state:
...........
...........
...........
...........
..1........
...........
...........

After 1 second:
...........
....1......
...........
...........
...........
...........
...........

After 2 seconds:
...........
...........
...........
...........
...........
......1....
...........

After 3 seconds:
...........
...........
........1..
...........
...........
...........
...........

After 4 seconds:
...........
...........
...........
...........
...........
...........
..........1

After 5 seconds:
...........
...........
...........
.1.........
...........
...........
...........
The Historian can't wait much longer, so you don't have to simulate the robots for very long. Where will the robots be after 100 seconds?

In the above example, the number of robots on each tile after 100 seconds has elapsed looks like this:

......2..1.
...........
1..........
.11........
.....1.....
...12......
.1....1....
To determine the safest area, count the number of robots in each quadrant after 100 seconds. Robots that are exactly in the middle (horizontally or vertically) don't count as being in any quadrant, so the only relevant robots are:

..... 2..1.
..... .....
1.... .....

..... .....
...12 .....
.1... 1....
In this example, the quadrants contain 1, 3, 4, and 1 robot. Multiplying these together gives a total safety factor of 12.

Predict the motion of the robots in your list within a space which is 101 tiles wide and 103 tiles tall. What will the safety factor be after exactly 100 seconds have elapsed?
'''

import re

# max_x = 11
# max_y = 7
max_x = 101
max_y = 103
# with open('input/14-small.txt', 'r') as f:
with open('input/14.txt', 'r') as f:
    lines = f.readlines()
lines = [l.rstrip() for l in lines if len(l) > 3]

def parse_line(line):
    '''
    >>> parse_line('p=43,88 v=84,88')
    [[43, 88], [84, 88]]

    >>> parse_line('p=53,1 v=-82,-40')
    [[53, 1], [-82, -40]]
    '''
    group = re.findall('p=(\d+),(\d+) v=(-?\d+),(-?\d+)', line)

    p = [[int(f[0]), int(f[1])] for f in group]
    v = [[int(f[2]), int(f[3])] for f in group]

    return [p[0], v[0]]

def get_new_coords(coord, mx):
    '''
    >>> get_new_coords(83, max_x)
    83

    >>> get_new_coords(-5, max_x)
    96

    >>> get_new_coords(132, max_x)
    31
    '''
    new_coord = coord
    if coord >= mx:
        new_coord = coord - mx
    if coord < 0:
        new_coord = mx + coord
    return new_coord

def move_robot(robot):
    '''
    >>> move_robot([[43, 88], [84, 88]])
    [26, 73]

    >>> move_robot([[67, 26], [-47, -53]])
    [20, 76]

    >>> move_robot([[17, 53], [-73, -73]])
    [45, 83]
    '''
    new_x = get_new_coords(robot[0][0] + robot[1][0], max_x)
    new_y = get_new_coords(robot[0][1] + robot[1][1], max_y)
    return [new_x, new_y]

pos = []
velocity = []
for l in lines:
    xy, vv = parse_line(l)
    pos.append(xy)
    velocity.append(vv)

for t in range(100):
    new_pos = []
    for id in range(len(pos)):
        xy = move_robot( (pos[id], velocity[id]) )
        new_pos.append(xy)
    pos = new_pos

half_x, half_y = max_x // 2, max_y // 2
counts = [0, 0, 0, 0]
for x, y in pos:
    if x < half_x and y < half_y:
        counts[0] += 1
    elif x > half_x and y < half_y:
        counts[1] += 1
    elif x < half_x and y > half_y:
        counts[2] += 1
    elif x > half_x and y > half_y:
        counts[3] += 1
    else:
        pass

ans = counts[0] * counts[1] * counts[2] * counts[3]
print('===============================')
print('The answer: ', ans)
print('===============================')
