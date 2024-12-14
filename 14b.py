#!/usr/bin/python3

# python3 -m doctest -v 14.py

'''
--- Part Two ---

During the bathroom break, someone notices that these robots seem awfully similar to ones built and used at the North Pole. If they're the same type of robots, they should have a hard-coded Easter egg: very rarely, most of the robots should arrange themselves into a picture of a Christmas tree.

What is the fewest number of seconds that must elapse for the robots to display the Easter egg?
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

def print_field():
    field = [[0 for _ in range(max_x)] for _ in range(max_y)]
    for x, y in pos:
        field[y][x] += 1
    for l in field:
        s = ''.join([str(v) if v > 0 else ' ' for v in l])
        print(s)

cnt = 0
while True:
    cnt += 1
    new_pos = []
    for id in range(len(pos)):
        xy = move_robot( (pos[id], velocity[id]) )
        new_pos.append(xy)
    pos = new_pos
    if cnt > 6256 and (cnt - 6256) % 101 == 0:
        print_field()
        e = input(f"time: {cnt}")
# --
# time: 5751
# time: 6436

# |
# time: 6256
# time: 6357
# time: 6458
# time: 6559

# time: 7569
