#!/usr/bin/python3

# python3 -m doctest -v 10b.py

'''
--- Part Two ---

The reindeer spends a few minutes reviewing your hiking trail map before realizing something, disappearing for a few minutes, and finally returning with yet another slightly-charred piece of paper.

The paper describes a second way to measure a trailhead called its rating. A trailhead's rating is the number of distinct hiking trails which begin at that trailhead. For example:

.....0.
..4321.
..5..2.
..6543.
..7..4.
..8765.
..9....
The above map has a single trailhead; its rating is 3 because there are exactly three distinct hiking trails which begin at that position:

.....0.   .....0.   .....0.
..4321.   .....1.   .....1.
..5....   .....2.   .....2.
..6....   ..6543.   .....3.
..7....   ..7....   .....4.
..8....   ..8....   ..8765.
..9....   ..9....   ..9....
Here is a map containing a single trailhead with rating 13:

..90..9
...1.98
...2..7
6543456
765.987
876....
987....
This map contains a single trailhead with rating 227 (because there are 121 distinct hiking trails that lead to the 9 on the right edge and 106 that lead to the 9 on the bottom edge):

012345
123456
234567
345678
4.6789
56789.
Here's the larger example from before:

89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
Considering its trailheads in reading order, they have ratings of 20, 24, 10, 4, 1, 4, 5, 8, and 5. The sum of all trailhead ratings in this larger example topographic map is 81.

You're not sure how, but the reindeer seems to have crafted some tiny flags out of toothpicks and bits of paper and is using them to mark trailheads on your topographic map. What is the sum of the ratings of all trailheads?
'''

from collections import deque, defaultdict

with open('input/10.txt', 'r') as f:
# with open('input/10-small.txt', 'r') as f:
    lines = f.readlines()
lines = [l.rstrip() for l in lines]
lines = [[int(ch) for ch in l] for l in lines]

q = deque()
for y in range(len(lines)):
    for x in range(len(lines[0])):
        if lines[y][x] == 0:
            q.append( (x, y, 0, x, y) )

found = defaultdict(list)
dxdy = [(0, -1), (1, 0), (0, 1), (-1, 0)]
while len(q) > 0:
    headx, heady, curr, cx, cy = q.popleft()
    if curr == 9:
        found[(headx, heady)].append( (cx, cy) ) # can be duplicate end via different path
    else:
        next = curr + 1
        candidates = [(cx + dx, cy + dy) for dx, dy in dxdy]
        valid = [(x, y) for x,y  in candidates if 0 <= x < len(lines[0]) and 0 <= y < len(lines)]
        for x, y in valid:
            if next == lines[y][x]:
                q.append((headx, heady, next, x, y))

total = 0
for _, pp in found.items():
    total += len(pp)
print('===============================')
print('The answer: ', total)
print('===============================')
