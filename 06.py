#!/usr/bin/python3

# python3 -m doctest -v 06.py

'''
--- Day 6: Guard Gallivant ---

The Historians use their fancy device again, this time to whisk you all away to the North Pole prototype suit manufacturing lab... in the year 1518! It turns out that having direct access to history is very convenient for a group of historians.

You still have to be careful of time paradoxes, and so it will be important to avoid anyone from 1518 while The Historians search for the Chief. Unfortunately, a single guard is patrolling this part of the lab.

Maybe you can work out where the guard will go ahead of time so that The Historians can search safely?

You start by making a map (your puzzle input) of the situation. For example:

....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
The map shows the current position of the guard with ^ (to indicate the guard is currently facing up from the perspective of the map). Any obstructions - crates, desks, alchemical reactors, etc. - are shown as #.

Lab guards in 1518 follow a very strict patrol protocol which involves repeatedly following these steps:

If there is something directly in front of you, turn right 90 degrees.
Otherwise, take a step forward.
Following the above protocol, the guard moves up several times until she reaches an obstacle (in this case, a pile of failed suit prototypes):

....#.....
....^....#
..........
..#.......
.......#..
..........
.#........
........#.
#.........
......#...
Because there is now an obstacle in front of the guard, she turns right before continuing straight in her new facing direction:

....#.....
........>#
..........
..#.......
.......#..
..........
.#........
........#.
#.........
......#...
Reaching another obstacle (a spool of several very long polymers), she turns right again and continues downward:

....#.....
.........#
..........
..#.......
.......#..
..........
.#......v.
........#.
#.........
......#...
This process continues for a while, but the guard eventually leaves the mapped area (after walking past a tank of universal solvent):

....#.....
.........#
..........
..#.......
.......#..
..........
.#........
........#.
#.........
......#v..
By predicting the guard's route, you can determine which specific positions in the lab will be in the patrol path. Including the guard's starting position, the positions visited by the guard before leaving the area are marked with an X:

....#.....
....XXXXX#
....X...X.
..#.X...X.
..XXXXX#X.
..X.X.X.X.
.#XXXXXXX.
.XXXXXXX#.
#XXXXXXX..
......#X..
In this example, the guard will visit 41 distinct positions on your map.

Predict the path of the guard. How many distinct positions will the guard visit before leaving the mapped area?
'''

import sys

# with open('input/06.txt', 'r') as f:
with open('input/06-small.txt', 'r') as f:
    lines = f.readlines()
field = [l.rstrip() for l in lines]

dir = '^>v<'
dxdy = [(0, -1), (1, 0), (0, 1), (-1, 0)]
def find_pos():
    for y in range(len(field)):
        for x in range(len(field[0])):
            ch = field[y][x]
            if ch in dir:
                return (x, y)
    print('@@@@@@@@@@')
    print('Cannot find init pos')
    print('@@@@@@@@@@')
    sys.exit(3)

def is_valid(pos):
    x, y = pos
    return 0 <= x < len(field[0]) and 0 <= y < len(field)

visited = set()
pos = find_pos()
d = field[pos[1]][pos[0]]
while is_valid(pos):
    visited.add(pos)
    x, y = pos
    id = dir.find(d)
    dx, dy = dxdy[id]
    new_x, new_y = x + dx, y + dy
    new_pos = (new_x, new_y)
    if is_valid(new_pos):
        if field[new_y][new_x] == '#':
            new_pos = pos
            new_id = (id + 1) % len(dir)
            d = dir[new_id]
    pos = new_pos

print('===============================')
print('The answer: ', len(visited))
print('===============================')
