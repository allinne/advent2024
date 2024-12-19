#!/usr/bin/python3

# python3 -m doctest -v 19.py

'''
--- Part Two ---

The staff don't really like some of the towel arrangements you came up with. To avoid an endless cycle of towel rearrangement, maybe you should just give them every possible option.

Here are all of the different ways the above example's designs can be made:

brwrr can be made in two different ways: b, r, wr, r or br, wr, r.

bggr can only be made with b, g, g, and r.

gbbr can be made 4 different ways:

g, b, b, r
g, b, br
gb, b, r
gb, br
rrbgbr can be made 6 different ways:

r, r, b, g, b, r
r, r, b, g, br
r, r, b, gb, r
r, rb, g, b, r
r, rb, g, br
r, rb, gb, r
bwurrg can only be made with bwu, r, r, and g.

brgr can be made in two different ways: b, r, g, r or br, g, r.

ubwu and bbrgwb are still impossible.

Adding up all of the ways the towels in this example could be arranged into the desired designs yields 16 (2 + 1 + 4 + 6 + 1 + 2).

They'll let you into the onsen as soon as you have the list. What do you get if you add up the number of different ways you could make each design?
'''

import datetime
from functools import lru_cache

def inp(fn):
    with open(fn, 'r') as f:
        lines = f.readlines()
    return [l.rstrip() for l in lines]

# f1 = inp('input/19-small.txt')
f1 = inp('input/19.txt')

towels = [t for t in f1[0].split(', ')]
designs = f1[2:]

def sort_towels_by_length(towels):
    return sorted(towels, key=len, reverse=True)

towels = sort_towels_by_length(towels)
print('towels: ', sort_towels_by_length(towels))

@lru_cache(maxsize=32_000_000_000)
def count(design):
    c = 0
    for t in towels:
        if design.startswith(t):
            design2 = design.replace(t, '', 1)
            if len(design2) > 0:
                c2 = count(design2)
                c += c2
            else:
                c += 1
    return c

total = 0
for id, d in enumerate(designs):
    print(datetime.datetime.now(), f'Starting design {id+1}: {d}')
    c = count(d)
    total += c
    print(datetime.datetime.now(), c, total)

print('===============================')
print('The answer: ', total) # 724_388_733_465_031
print('===============================')
