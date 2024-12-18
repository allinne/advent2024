#!/usr/bin/python3

# python3 -m doctest -v 18.py

'''
--- Day 18: RAM Run ---

You and The Historians look a lot more pixelated than you remember. You're inside a computer at the North Pole!

Just as you're about to check out your surroundings, a program runs up to you. "This region of memory isn't safe! The User misunderstood what a pushdown automaton is and their algorithm is pushing whole bytes down on top of us! Run!"

The algorithm is fast - it's going to cause a byte to fall into your memory space once every nanosecond! Fortunately, you're faster, and by quickly scanning the algorithm, you create a list of which bytes will fall (your puzzle input) in the order they'll land in your memory space.

Your memory space is a two-dimensional grid with coordinates that range from 0 to 70 both horizontally and vertically. However, for the sake of example, suppose you're on a smaller grid with coordinates that range from 0 to 6 and the following list of incoming byte positions:

5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0
Each byte position is given as an X,Y coordinate, where X is the distance from the left edge of your memory space and Y is the distance from the top edge of your memory space.

You and The Historians are currently in the top left corner of the memory space (at 0,0) and need to reach the exit in the bottom right corner (at 70,70 in your memory space, but at 6,6 in this example). You'll need to simulate the falling bytes to plan out where it will be safe to run; for now, simulate just the first few bytes falling into your memory space.

As bytes fall into your memory space, they make that coordinate corrupted. Corrupted memory coordinates cannot be entered by you or The Historians, so you'll need to plan your route carefully. You also cannot leave the boundaries of the memory space; your only hope is to reach the exit.

In the above example, if you were to draw the memory space after the first 12 bytes have fallen (using . for safe and # for corrupted), it would look like this:

...#...
..#..#.
....#..
...#..#
..#..#.
.#..#..
#.#....
You can take steps up, down, left, or right. After just 12 bytes have corrupted locations in your memory space, the shortest path from the top left corner to the exit would take 22 steps. Here (marked with O) is one such path:

OO.#OOO
.O#OO#O
.OOO#OO
...#OO#
..#OO#.
.#.O#..
#.#OOOO
Simulate the first kilobyte (1024 bytes) falling onto your memory space. Afterward, what is the minimum number of steps needed to reach the exit?
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
# n_obstacles = 12 # for 18a this set in stone
n_obstacles = 1024 # for 18a this set in stone

opairs = f1[:n_obstacles]
obstacles = []
for xy in opairs:
    xs, ys = xy.split(',')
    obstacles.append((int(xs), int(ys)))

step_blocked = {} # step, set( (x,y) )
def is_blocked(x, y, step): # 0 <= step < 1023
    blocked = False
    if step >= n_obstacles:
        step = n_obstacles - 1
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

for k in range(n_obstacles):
    _ = is_blocked(0, 0, k)

def print_field(field):
    for s in field:
        print(''.join(str(c) for c in s))

def print_path(step, apath):
    field = [['.' for x in range(size)] for y in range(size)]
    if not step in step_blocked:
        b = is_blocked(0, 0, step)
    if not step in step_blocked:
        step = n_obstacles - 1
    for x, y in step_blocked[step]:
        field[y][x] = '#'
    for x, y in apath:
        if field[y][x] == '#':
            field[y][x] = 'X'
        else:
            field[y][x] = 'O'
    print_field(field)

def path():
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
        # print(x, y, step)
        # print_path(step, path)
        # print(16*'-')

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
                            if not is_blocked(nx, ny, n_obstacles) and not (nx, ny) in visited:
                                npath = path[:]
                                npath.append((nx, ny))
                                heapq.heappush(q, (nstep, (nx, ny, npath)))
                                visited.add((nx, ny))
    return best, best_path

best, best_path = path()
print_path(best, best_path)
print('===============================')
print('The answer: ', best)
print('===============================')
