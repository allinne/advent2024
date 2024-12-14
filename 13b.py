#!/usr/bin/python3

# python3 -m doctest -v 13b.py

'''
--- Part Two ---

As you go to win the first prize, you discover that the claw is nowhere near where you expected it would be. Due to a unit conversion error in your measurements, the position of every prize is actually 10000000000000 higher on both the X and Y axis!

Add 10000000000000 to the X and Y position of every prize. After making this change, the example above would now look like this:

Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=10000000008400, Y=10000000005400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=10000000012748, Y=10000000012176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=10000000007870, Y=10000000006450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=10000000018641, Y=10000000010279
Now, it is only possible to win a prize on the second and fourth claw machines. Unfortunately, it will take many more than 100 presses to do so.

Using the corrected prize coordinates, figure out how to win as many prizes as possible. What is the fewest tokens you would have to spend to win all possible prizes?
'''

import re

# with open('input/13-small.txt', 'r') as f:
with open('input/13.txt', 'r') as f:
    strs = f.readlines()
strs = [l.rstrip() for l in strs if len(l) > 3]

def get_x_y(line):
    '''
    >>> get_x_y('Button A: X+94, Y+34')
    [94, 34]

    >>> get_x_y('Button B: X+22, Y+67')
    [22, 67]

    >>> get_x_y('Prize: X=8400, Y=5400')
    [8400, 5400]
    '''
    groups = re.findall('X[+=](\d+)\, Y[+=](\d+)', line)
    x_y = [ [int(f[0]), int(f[1])] for f in groups]
    return x_y[0]

def parse_lines(lines):
    '''
    >>> parse_lines(['Button A: X+94, Y+34', 'Button B: X+22, Y+67', 'Prize: X=8400, Y=5400'])
    [[[94, 34], [22, 67], [10000000008400, 10000000005400]]]
    '''
    k = 0
    data = []
    summator = 10_000_000_000_000
    for id in range(0, len(lines), 3):
        data.append([[], [], []])
        if lines[id].find('Button A') > -1:
            x, y = get_x_y(lines[id])
            data[k][0] = [x, y]
        if lines[id+1].find('Button B') > -1:
            x, y = get_x_y(lines[id+1])
            data[k][1] = [x, y]
        if lines[id+2].find('Prize') > -1:
            x, y = get_x_y(lines[id+2])
            data[k][2] = [x+summator, y+summator]
            k += 1
    return data

inp = parse_lines(strs)

total = 0
for rec in inp:
    min_token = 10000000000001*10000000000001
    xy_a, xy_b, target = rec
    AX, AY = xy_a
    BX, BY = xy_b
    X, Y = target

    if Y * BX == X * BY: # tan B = tan Target
        if X % BX ==0 and Y % BY == 0: # b only
            b = X // BX
            b1 = Y // BY
            assert b == b1, f'{rec}'
            min_token = b
        else:
            # since b points exactly to the target, only a pointing exactly to the target can be suitable
            if Y * AX == X * AY: # a also to the target
                rem = X % BX
                b = X // BX
                for mb in range(10_000):
                    # doing x only as both a,b speed is the same
                    if (rem + BX * mb) % AX == 0:
                        b1 = b - mb
                        a = (rem + BX * mb) // AX
                        min_token = b1 + 3 * a # cost(a) is 3
                        break # found
            else: # upper/lower a cannot be valid
                continue
    # b not to the target
    elif X * BY < Y * BX: # b below: BX is faster
        # only different sided can make it
        if X * AY > Y * AX:
            # only one solution possible
            # both x,y must be found
            ka = AY / AX
            kb = BY / BX
            ba = 0
            bb = Y - kb * X
            x1 = (bb - ba) / (ka - kb)
            y1 = ka * x1 + ba
            a1 = y1 / AY
            a2 = int(a1)
            mb1 = (X - x1) / BX
            mb2 = int(mb1)
            tolerance = 200
            a_start = a2 - tolerance
            if a_start < 0: a_start = 0
            b_start = mb2 - tolerance
            if b_start < 0: b_start = 0
            for a in range(a_start, a_start + tolerance + tolerance):
                for b in range(b_start, b_start + tolerance + tolerance):
                    if X == a * AX + b * BX and Y == a * AY + b * BY:
                        min_token = b + 3 * a # cost(a) is 3
                        break
                if min_token <  10000000000001*10000000000001:
                    break

    else: # b above: BY is faster
        if X * AY < Y * AX: # a below
            # only one solution possible
            # both x,y must be found
            ka = AY / AX
            kb = BY / BX
            ba = Y - ka * X
            bb = 0
            x1 = (ba - bb) / (kb - ka)
            y1 = kb * x1 + bb
            b1 = y1 / BY
            b2 = int(b1)
            ma1 = (X - x1) / AX
            ma2 = int(ma1)
            tolerance = 200
            a_start = ma2 - tolerance
            if a_start < 0: a_start = 0
            b_start = b2 - tolerance
            if b_start < 0: b_start = 0
            for a in range(a_start, a_start + tolerance + tolerance):
                for b in range(b_start, b_start + tolerance + tolerance):
                    if X == a * AX + b * BX and Y == a * AY + b * BY:
                        min_token = b + 3 * a # cost(a) is 3
                        break
                if min_token <  10000000000001*10000000000001:
                    break

    print('@@@@@@', min_token)
    if min_token < 10000000000001*10000000000001:
        total += min_token

print('===============================')
print('The answer: ', total)
print('===============================')
