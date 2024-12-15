#!/usr/bin/python3

# python3 -m doctest -v 15b.py

'''
--- Part Two ---

The lanternfish use your information to find a safe moment to swim in and turn off the malfunctioning robot! Just as they start preparing a festival in your honor, reports start coming in that a second warehouse's robot is also malfunctioning.

This warehouse's layout is surprisingly similar to the one you just helped. There is one key difference: everything except the robot is twice as wide! The robot's list of movements doesn't change.

To get the wider warehouse's map, start with your original map and, for each tile, make the following changes:

If the tile is #, the new map contains ## instead.
If the tile is O, the new map contains [] instead.
If the tile is ., the new map contains .. instead.
If the tile is @, the new map contains @. instead.
This will produce a new warehouse map which is twice as wide and with wide boxes that are represented by []. (The robot does not change size.)

The larger example from before would now look like this:

####################
##....[]....[]..[]##
##............[]..##
##..[][]....[]..[]##
##....[]@.....[]..##
##[]##....[]......##
##[]....[]....[]..##
##..[][]..[]..[][]##
##........[]......##
####################
Because boxes are now twice as wide but the robot is still the same size and speed, boxes can be aligned such that they directly push two other boxes at once. For example, consider this situation:

#######
#...#.#
#.....#
#..OO@#
#..O..#
#.....#
#######

<vv<<^^<<^^
After appropriately resizing this map, the robot would push around these boxes as follows:

Initial state:
##############
##......##..##
##..........##
##....[][]@.##
##....[]....##
##..........##
##############

Move <:
##############
##......##..##
##..........##
##...[][]@..##
##....[]....##
##..........##
##############

Move v:
##############
##......##..##
##..........##
##...[][]...##
##....[].@..##
##..........##
##############

Move v:
##############
##......##..##
##..........##
##...[][]...##
##....[]....##
##.......@..##
##############

Move <:
##############
##......##..##
##..........##
##...[][]...##
##....[]....##
##......@...##
##############

Move <:
##############
##......##..##
##..........##
##...[][]...##
##....[]....##
##.....@....##
##############

Move ^:
##############
##......##..##
##...[][]...##
##....[]....##
##.....@....##
##..........##
##############

Move ^:
##############
##......##..##
##...[][]...##
##....[]....##
##.....@....##
##..........##
##############

Move <:
##############
##......##..##
##...[][]...##
##....[]....##
##....@.....##
##..........##
##############

Move <:
##############
##......##..##
##...[][]...##
##....[]....##
##...@......##
##..........##
##############

Move ^:
##############
##......##..##
##...[][]...##
##...@[]....##
##..........##
##..........##
##############

Move ^:
##############
##...[].##..##
##...@.[]...##
##....[]....##
##..........##
##..........##
##############
This warehouse also uses GPS to locate the boxes. For these larger boxes, distances are measured from the edge of the map to the closest edge of the box in question. So, the box shown below has a distance of 1 from the top edge of the map and 5 from the left edge of the map, resulting in a GPS coordinate of 100 * 1 + 5 = 105.

##########
##...[]...
##........
In the scaled-up version of the larger example from above, after the robot has finished all of its moves, the warehouse would look like this:

####################
##[].......[].[][]##
##[]...........[].##
##[]........[][][]##
##[]......[]....[]##
##..##......[]....##
##..[]............##
##..@......[].[][]##
##......[][]..[]..##
####################
The sum of these boxes' GPS coordinates is 9021.

Predict the motion of the robot and boxes in this new, scaled-up warehouse. What is the sum of all boxes' final GPS coordinates?
'''

from collections import deque

def inp(fn):
    with open(fn, 'r') as f:
        lines = f.readlines()
    return [l.rstrip() for l in lines]

def print_field(field):
    for s in field:
        print(''.join(s))

def parse(lines):
    field = []
    for l in lines:
        if len(l) < 2:
            break
        if l[0] == '#':
            s = []
            for ch in l:
                if ch == '#':
                    s.append('#')
                    s.append('#')
                if ch == 'O':
                    s.append('[')
                    s.append(']')
                if ch == '.':
                    s.append('.')
                    s.append('.')
                if ch == '@':
                    s.append('@')
                    s.append('.')
            field.append(s)
    moves = ''.join([s.strip() for s in lines[len(field):] if len(s.strip()) > 1])
    return field, moves

def proceed(field, moves):
    fx, fy = 0, 0
    for x in range(len(field[0])):
        for y in range(len(field)):
            if field[y][x] == '@':
                fx = x
                fy = y
                break
    for move in moves:
        if move == '>':
            to_move = set()
            to_move.add((fx, fy))
            blocked = False
            front = deque()
            front.append((fx+1, fy))
            while not blocked and len(front) > 0:
                x, y = front.pop()
                cell = field[y][x]
                if cell == '#':
                    blocked = True
                else:
                    if cell == '.':
                        continue
                    elif cell == '[':
                        to_move.add((x, y))
                        to_move.add((x+1, y))
                        front.append((x+2, y))

            if not blocked:
                a = list(to_move)
                b = reversed(sorted(a))
                for x, y in b:
                    field[y][x+1] = field[y][x]
                    field[y][x] = '.'
                fx += 1

        if move == 'v':
            to_move = set()
            to_move.add((fx, fy))
            blocked = False
            front = deque()
            front.append((fx, fy+1))
            while not blocked and len(front) > 0:
                x, y = front.pop()
                cell = field[y][x]
                if cell == '#':
                    blocked = True
                else:
                    if cell == '.':
                        continue
                    elif cell == '[':
                        to_move.add((x, y))
                        to_move.add((x+1, y))
                        front.append((x, y+1))
                        front.append((x+1, y+1))
                    elif cell == ']':
                        to_move.add((x, y))
                        to_move.add((x-1, y))
                        front.append((x, y+1))
                        front.append((x-1, y+1))

            if not blocked:
                a = list(to_move)
                b = reversed(sorted(a))
                for x, y in b:
                    field[y+1][x] = field[y][x]
                    field[y][x] = '.'
                fy += 1

        if move == '<':
            to_move = set()
            to_move.add((fx, fy))
            blocked = False
            front = deque()
            front.append((fx-1, fy))
            while not blocked and len(front) > 0:
                x, y = front.pop()
                cell = field[y][x]
                if cell == '#':
                    blocked = True
                else:
                    if cell == '.':
                        continue
                    elif cell == ']':
                        to_move.add((x, y))
                        to_move.add((x-1, y))
                        front.append((x-2, y))

            if not blocked:
                a = list(to_move)
                b = sorted(a)
                for x, y in b:
                    field[y][x-1] = field[y][x]
                    field[y][x] = '.'
                fx -= 1

        if move == '^':
            to_move = set()
            to_move.add((fx, fy))
            blocked = False
            front = deque()
            front.append((fx, fy-1))
            while not blocked and len(front) > 0:
                x, y = front.pop()
                cell = field[y][x]
                if cell == '#':
                    blocked = True
                else:
                    if cell == '.':
                        continue
                    elif cell == '[':
                        to_move.add((x, y))
                        to_move.add((x+1, y))
                        front.append((x, y-1))
                        front.append((x+1, y-1))
                    elif cell == ']':
                        to_move.add((x, y))
                        to_move.add((x-1, y))
                        front.append((x, y-1))
                        front.append((x-1, y-1))

            if not blocked:
                a = list(to_move)
                b = sorted(a)
                for x, y in b:
                    field[y-1][x] = field[y][x]
                    field[y][x] = '.'
                fy -= 1
    return field

def calc_gps(field):
    total = 0
    for x in range(len(field[0])):
        for y in range(len(field)):
            if field[y][x] == '[':
                total += y*100 + x
    return total

# f1 = inp('input/15-small-00.txt')
# f1 = inp('input/15-small-01.txt')
# f1 = inp('input/15-small.txt')
f1 = inp('input/15.txt')
field, moves = parse(f1)
transformed = proceed(field, moves)
sum = calc_gps(transformed)
print('===============================')
print('The answer: ', sum)
print('===============================')
