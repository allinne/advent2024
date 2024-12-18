#!/usr/bin/python3

# python3 -m doctest -v 18b.py

'''
--- Part Two ---

The Historians aren't as used to moving around in this pixelated universe as you are. You're afraid they're not going to be fast enough to make it to the exit before the path is completely blocked.

To determine how fast everyone needs to go, you need to determine the first byte that will cut off the path to the exit.

In the above example, after the byte at 1,1 falls, there is still a path to the exit:

O..#OOO
O##OO#O
O#OO#OO
OOO#OO#
###OO##
.##O###
#.#OOOO
However, after adding the very next byte (at 6,1), there is no longer a path to the exit:

...#...
.##..##
.#..#..
...#..#
###..##
.##.###
#.#....
So, in this example, the coordinates of the first byte that prevents the exit from being reachable are 6,1.

Simulate more of the bytes that are about to corrupt your memory space. What are the coordinates of the first byte that will prevent the exit from being reachable from your starting position? (Provide the answer as two integers separated by a comma with no other characters.)
'''

import datetime, heapq, sys

def inp(fn):
    with open(fn, 'r') as f:
        lines = f.readlines()
    return [l.rstrip() for l in lines if len(l) > 2]

# f1 = inp('input/18-small.txt')
f1 = inp('input/18.txt')
# size = 7
size = 71

obstacles = []
for xy in f1:
    xs, ys = xy.split(',')
    obstacles.append((int(xs), int(ys)))

step_blocked = {} # step, set( (x,y) )
def is_blocked(x, y, step): # 0 <= step < 1023
    blocked = False
    if not step in step_blocked:
        if step > 0:
            blocked = is_blocked(x, y, step - 1)
            sb = {obstacles[step]}
            for o in step_blocked[step - 1]:
                sb.add(o)
            step_blocked[step] = sb
        else:
            step_blocked[0] = {obstacles[0]}
    if not blocked:
        blocked = True if (x, y) in step_blocked[step] else False
    return blocked

for k in range(len(f1)):
    _ = is_blocked(0, 0, k)

def print_field(field):
    for s in field:
        print(''.join(str(c) for c in s))

def print_path(step, apath):
    field = [['.' for x in range(size)] for y in range(size)]
    if not step in step_blocked:
        b = is_blocked(0, 0, step)
    if not step in step_blocked:
        step = len(f1) - 1
    for x, y in step_blocked[step]:
        field[y][x] = '#'
    for x, y in apath:
        if field[y][x] == '#':
            field[y][x] = 'X'
        else:
            field[y][x] = 'O'
    print_field(field)

def path(no):
    # dir_ch = '^>v<'
    dxdy = [(0, -1), (1, 0), (0, 1), (-1, 0)]

    q = [] # step, rest
    heapq.heappush(q, (0, (0, 0, [(0, 0)]))) # step, (x, y, path)
    visited = {(0,0)}
    best = 100000000000000
    best_path = []
    while len(q) > 0:
        step, rest = heapq.heappop(q)
        x, y, path = rest

        if step < best:
            if x == size - 1 and y == size - 1:
                best = step
                best_path = path
            else:
                nstep = step + 1
                if nstep < best:
                    nxy = [(x+dx, y+dy) for dx, dy in dxdy]
                    for nx, ny in nxy:
                        if 0 <= nx < size and 0 <= ny < size:
                            if not is_blocked(nx, ny, no) and not (nx, ny) in visited:
                                npath = path[:]
                                npath.append((nx, ny))
                                heapq.heappush(q, (nstep, (nx, ny, npath)))
                                visited.add((nx, ny))
    return best, best_path

for k in range(len(f1)):
    best, best_path = path(k)
    if best >= 100000000000000:
        # print_path(k, best_path)
        print('===============================')
        print('The answer: ', k+1, f1[k])
        print('===============================')
        sys.exit(0)

print("@@@@@")
