#!/usr/bin/python3

# python3 -m doctest -v 11b.py

'''
--- Day 11: Plutonian Pebbles ---

The ancient civilization on Pluto was known for its ability to manipulate spacetime, and while The Historians explore their infinite corridors, you've noticed a strange set of physics-defying stones.

At first glance, they seem like normal stones: they're arranged in a perfectly straight line, and each stone has a number engraved on it.

The strange part is that every time you blink, the stones change.

Sometimes, the number engraved on a stone changes. Other times, a stone might split in two, causing all the other stones to shift over a bit to make room in their perfectly straight line.

As you observe them for a while, you find that the stones have a consistent behavior. Every time you blink, the stones each simultaneously change according to the first applicable rule in this list:

If the stone is engraved with the number 0, it is replaced by a stone engraved with the number 1.
If the stone is engraved with a number that has an even number of digits, it is replaced by two stones. The left half of the digits are engraved on the new left stone, and the right half of the digits are engraved on the new right stone. (The new numbers don't keep extra leading zeroes: 1000 would become stones 10 and 0.)
If none of the other rules apply, the stone is replaced by a new stone; the old stone's number multiplied by 2024 is engraved on the new stone.
No matter how the stones change, their order is preserved, and they stay on their perfectly straight line.

How will the stones evolve if you keep blinking at them? You take a note of the number engraved on each stone in the line (your puzzle input).

If you have an arrangement of five stones engraved with the numbers 0 1 10 99 999 and you blink once, the stones transform as follows:

The first stone, 0, becomes a stone marked 1.
The second stone, 1, is multiplied by 2024 to become 2024.
The third stone, 10, is split into a stone marked 1 followed by a stone marked 0.
The fourth stone, 99, is split into two stones marked 9.
The fifth stone, 999, is replaced by a stone marked 2021976.
So, after blinking once, your five stones would become an arrangement of seven stones engraved with the numbers 1 2024 1 0 9 9 2021976.


--- Part Two ---

The Historians sure are taking a long time. To be fair, the infinite corridors are very large.

How many stones would you have after blinking a total of 75 times?
'''

from collections import defaultdict

with open('input/11.txt', 'r') as f:
# with open('input/11-small.txt', 'r') as f:
    lines = f.readlines()
lines = [l.rstrip() for l in lines]

def transform(stone):
    '''
    >>> transform(0)
    [1]

    >>> transform(1)
    [2024]

    >>> transform(10)
    [1, 0]

    >>> transform(99)
    [9, 9]

    >>> transform(999)
    [2021976]
    '''
    if stone == 0:
        return [1]

    s = str(stone)
    if len(s) % 2 == 0:
        pos = len(s) // 2
        left = int(s[:pos])
        right = int(s[pos:])
        return [left, right]
    return [stone * 2024]

def squash_mul(stones, muls):
    '''
    >>> squash_mul([4, 0, 4, 8, 20, 24, 4, 0, 4, 8, 8, 0, 9, 6], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
    ([0, 4, 6, 8, 9, 20, 24], [3, 4, 1, 3, 1, 1, 1])

    >>> squash_mul([4, 0, 4, 8, 20, 24, 4, 0, 4, 8, 8, 0, 9, 6], [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
    ([0, 4, 6, 8, 9, 20, 24], [3, 5, 1, 3, 1, 1, 1])
    '''
    num_cnt = defaultdict(int)
    for id in range(len(stones)):
        n = stones[id]
        m = muls[id]
        num_cnt[n] += m
    kv = [(k, v) for k, v in num_cnt.items()]
    kv.sort()
    nums = [i[0] for i in kv]
    counts = [i[1] for i in kv]
    return nums, counts

n = 75
stones = [int(s) for s in lines[0].split()]
counts = [1 for s in stones]
for k in range(n):
    out_stones = []
    out_counts = []
    for id in range(len(stones)):
        s, cnt = stones[id], counts[id]
        out = transform(s)
        out_cnt = [cnt for i in range(len(out))]
        out_stones += out
        out_counts += out_cnt
    squashed, squashed_counts = squash_mul(out_stones, out_counts)
    stones = squashed
    counts = squashed_counts

total = 0
for v in counts:
    total += v

print('===============================')
print('The answer: ', total)
print('===============================')
