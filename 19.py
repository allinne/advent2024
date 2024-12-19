#!/usr/bin/python3

# python3 -m doctest -v 19.py

'''
--- Day 19: Linen Layout ---

Today, The Historians take you up to the hot springs on Gear Island! Very suspiciously, absolutely nothing goes wrong as they begin their careful search of the vast field of helixes.

Could this finally be your chance to visit the onsen next door? Only one way to find out.

After a brief conversation with the reception staff at the onsen front desk, you discover that you don't have the right kind of money to pay the admission fee. However, before you can leave, the staff get your attention. Apparently, they've heard about how you helped at the hot springs, and they're willing to make a deal: if you can simply help them arrange their towels, they'll let you in for free!

Every towel at this onsen is marked with a pattern of colored stripes. There are only a few patterns, but for any particular pattern, the staff can get you as many towels with that pattern as you need. Each stripe can be white (w), blue (u), black (b), red (r), or green (g). So, a towel with the pattern ggr would have a green stripe, a green stripe, and then a red stripe, in that order. (You can't reverse a pattern by flipping a towel upside-down, as that would cause the onsen logo to face the wrong way.)

The Official Onsen Branding Expert has produced a list of designs - each a long sequence of stripe colors - that they would like to be able to display. You can use any towels you want, but all of the towels' stripes must exactly match the desired design. So, to display the design rgrgr, you could use two rg towels and then an r towel, an rgr towel and then a gr towel, or even a single massive rgrgr towel (assuming such towel patterns were actually available).

To start, collect together all of the available towel patterns and the list of desired designs (your puzzle input). For example:

r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb
The first line indicates the available towel patterns; in this example, the onsen has unlimited towels with a single red stripe (r), unlimited towels with a white stripe and then a red stripe (wr), and so on.

After the blank line, the remaining lines each describe a design the onsen would like to be able to display. In this example, the first design (brwrr) indicates that the onsen would like to be able to display a black stripe, a red stripe, a white stripe, and then two red stripes, in that order.

Not all designs will be possible with the available towels. In the above example, the designs are possible or impossible as follows:

brwrr can be made with a br towel, then a wr towel, and then finally an r towel.
bggr can be made with a b towel, two g towels, and then an r towel.
gbbr can be made with a gb towel and then a br towel.
rrbgbr can be made with r, rb, g, and br.
ubwu is impossible.
bwurrg can be made with bwu, r, r, and g.
brgr can be made with br, g, and r.
bbrgwb is impossible.
In this example, 6 of the eight designs are possible with the available towel patterns.

To get into the onsen as soon as possible, consult your list of towel patterns and desired designs carefully. How many designs are possible?
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
def is_possible(design):
    '''
    >>> is_possible(['bwu', 'wr', 'rb', 'gb', 'br', 'r', 'b', 'g'], 'brwrr')
    True
    >>> is_possible(['bwu', 'wr', 'rb', 'gb', 'br', 'r', 'b', 'g'], 'ubwu')
    False
    >>> is_possible(['bwu', 'wr', 'rb', 'gb', 'br', 'r', 'b', 'g'], 'bwurrg')
    True
    >>> is_possible(['bwu', 'wr', 'rb', 'gb', 'br', 'r', 'b', 'g'], 'bbrgwb')
    False
    '''
    b = False
    for t in towels:
        if design.startswith(t):
            design2 = design.replace(t, '', 1)
            if len(design2) < 1 or is_possible(design2):
                b = True
                break
    return b

possible = 0
for id, d in enumerate(designs):
    print(datetime.datetime.now(), f'Starting design {id+1}: {d}')
    if is_possible(d):
        possible += 1
        word = 'Possible'
    else:
        word = 'Not'
    print(datetime.datetime.now(), word)

print('===============================')
print('The answer: ', possible)
print('===============================')
