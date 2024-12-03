#!/usr/bin/python3

# python3 -m doctest -v 02b.py

'''
The engineers are surprised by the low number of safe reports until they realize they forgot to tell you about the Problem Dampener.

The Problem Dampener is a reactor-mounted module that lets the reactor safety systems tolerate a single bad level in what would otherwise be a safe report. It's like the bad level never happened!

Now, the same rules apply as before, except if removing a single level from an unsafe report would make it safe, the report instead counts as safe.

More of the above example's reports are now safe:

7 6 4 2 1: Safe without removing any level.
1 2 7 8 9: Unsafe regardless of which level is removed.
9 7 6 2 1: Unsafe regardless of which level is removed.
1 3 2 4 5: Safe by removing the second level, 3.
8 6 4 4 1: Safe by removing the third level, 4.
1 3 6 7 9: Safe without removing any level.
Thanks to the Problem Dampener, 4 reports are actually safe!

Update your analysis by handling situations where the Problem Dampener can remove a single level from unsafe reports. How many reports are now safe?
'''

import sys

# with open('input/02-small.txt', 'r') as f:
with open('input/02.txt', 'r') as f:
    lines = f.readlines()
lines = [l.rstrip() for l in lines]

def parse_line(line):
    '''
    >>> parse_line('7 6 4 2 1')
    [7, 6, 4, 2, 1]
    '''

    return [int(s) for s in line.split()]

def get_sign(num):
    sign = 0
    if num < 0: sign = -1
    if num > 0: sign = 1
    return sign

def is_line_good(line):
    '''
    >>> is_line_good([24, 25, 28, 31, 28])
    (False, 3)

    >>> is_line_good([41, 44, 45, 48, 49, 50, 50])
    (False, 5)

    >>> is_line_good([11, 13, 16, 17, 19, 26])
    (False, 4)

    >>> is_line_good([11, 13, 16, 17, 19])
    (True, -1)

    >>> is_line_good([52, 53, 56, 57, 58])
    (True, -1)

    >>> is_line_good([54, 52, 53, 56, 57, 58])
    (False, 1)
    '''
    prev_sign = 0
    broken = -1
    is_good = True
    for i in range(len(line) - 1):
        d = line[i] - line[i+1]
        sign = get_sign(d)

        if i != 0 and prev_sign != sign:
            is_good = False
            broken = i
            break
        if abs(d) > 3 or abs(d) == 0:
            is_good = False
            broken = i
            break

        prev_sign = sign

    return (is_good, broken)

def check_line(line):
    '''
    >>> check_line([7, 6, 4, 2, 1])
    1
    >>> check_line([1, 2, 7, 8, 9])
    0
    >>> check_line([1, 3, 6, 7, 9])
    1
    >>> check_line([18, 15, 12, 9, 8, 6, 4, 1])
    1
    >>> check_line([32, 30, 32, 33, 34, 32])
    0

    >>> check_line([54, 52, 53, 56, 57, 58])
    1
    >>> check_line([94, 96, 94, 91, 88])
    1
    >>> check_line([12, 9, 12, 13, 15, 17, 20, 23])
    1
    >>> check_line([96, 98, 97, 95, 93, 90, 89])
    1
    '''

    safe = 0
    is_good, broken = is_line_good(line)
    if is_good:
        safe = 1
    else:
        cleaned = line[:broken] + line[broken + 1:] # cut this
        is_good, _ = is_line_good(cleaned)
        if is_good:
            safe = 1
        else:
            left = line[:broken + 1] # cut +1
            right = line[broken + 2:] if broken + 2 <= len(line) else []
            cleaned = left + right
            is_good, _ = is_line_good(cleaned)
            if is_good:
                safe = 1
            else:
                if broken > 0: # cut -1
                    left = line[:broken-1]
                    right = line[broken:] if broken + 1 <= len(line) else []
                    cleaned = left + right
                    is_good, _ = is_line_good(cleaned)
                    if is_good:
                        safe = 1
    return safe

good = 0
for l in lines:
    nums = parse_line(l)
    good += check_line(nums)

print('===============================')
print('The answer: ' + str(good))
print('===============================')
