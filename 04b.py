#!/usr/bin/python3

# python3 -m doctest -v 04b.py

'''
--- Part Two ---

The Elf looks quizzically at you. Did you misunderstand the assignment?

Looking for the instructions, you flip over the word search to find that this isn't actually an XMAS puzzle; it's an X-MAS puzzle in which you're supposed to find two MAS in the shape of an X. One way to achieve that is like this:

M.S
.A.
M.S
Irrelevant characters have again been replaced with . in the above diagram. Within the X, each MAS can be written forwards or backwards.

Here's the same example from before, but this time all of the X-MASes have been kept instead:

.M.S......
..A..MSMS.
.M.S.MAA..
..A.ASMSM.
.M.S.M....
..........
S.S.S.S.S.
.A.A.A.A..
M.M.M.M.M.
..........
In this example, an X-MAS appears 9 times.

Flip the word search from the instructions back over to the word search side and try again. How many times does an X-MAS appear?
'''

with open('input/04.txt', 'r') as f:
# with open('input/04-small.txt', 'r') as f:
    lines = f.readlines()
field = [l.rstrip() for l in lines]

patterns = {'MSSM', 'SMMS', 'SSMM', 'MMSS'}
dxdy = [(-1, -1), (1, -1), (1, 1), (-1, 1)]
total = 0
found = []
for y in range(1, len(field) - 1):
    for x in range(1, len(field[0]) - 1):
        if field[y][x] == 'A':
            corner_coords = [(x + dx, y + dy) for dx, dy in dxdy]
            corner_chars = [field[cy][cx] for cx, cy in corner_coords]
            s = "".join(corner_chars)
            if s in patterns:
                found.append(corner_coords)
                total += 1

print('===============================')
print('The answer:', total)
print('===============================')
