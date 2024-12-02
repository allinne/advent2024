#!/usr/bin/python3

# python3 -m doctest -v 02.py

'''
The unusual data (your puzzle input) consists of many reports, one report per line. Each report is a list of numbers called levels that are separated by spaces. For example:

7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
This example data contains six reports each containing five levels.

The engineers are trying to figure out which reports are safe. The Red-Nosed reactor safety systems can only tolerate levels that are either gradually increasing or gradually decreasing. So, a report only counts as safe if both of the following are true:

The levels are either all increasing or all decreasing.
Any two adjacent levels differ by at least one and at most three.
In the example above, the reports can be found safe or unsafe by checking those rules:

7 6 4 2 1: Safe because the levels are all decreasing by 1 or 2.
1 2 7 8 9: Unsafe because 2 7 is an increase of 5.
9 7 6 2 1: Unsafe because 6 2 is a decrease of 4.
1 3 2 4 5: Unsafe because 1 3 is increasing but 3 2 is decreasing.
8 6 4 4 1: Unsafe because 4 4 is neither an increase or a decrease.
1 3 6 7 9: Safe because the levels are all increasing by 1, 2, or 3.
So, in this example, 2 reports are safe.

Analyze the unusual data from the engineers. How many reports are safe?
'''

import re

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
    prev_sign = 0
    is_good = True
    for i in range(len(line) - 1):
        d = line[i] - line[i+1]
        sign = get_sign(d)

        if i != 0 and prev_sign != sign:
            is_good = False
            break
        if abs(d) > 3 or abs(d) == 0:
            is_good = False
            break

        prev_sign = sign

    return is_good

good = 0
for l in lines:
    line = parse_line(l)
    is_good = is_line_good(line)
    if is_good:
        good += 1


print('===============================')
print('The answer: ' + str(good))
print('===============================')
