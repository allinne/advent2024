#!/usr/bin/python3

# python3 -m doctest -v 12b.py

'''

--- Part Two ---

Fortunately, the Elves are trying to order so much fence that they qualify for a bulk discount!

Under the bulk discount, instead of using the perimeter to calculate the price, you need to use the number of sides each region has. Each straight section of fence counts as a side, regardless of how long it is.

Consider this example again:

AAAA
BBCD
BBCC
EEEC
The region containing type A plants has 4 sides, as does each of the regions containing plants of type B, D, and E. However, the more complex region containing the plants of type C has 8 sides!

Using the new method of calculating the per-region price by multiplying the region's area by its number of sides, regions A through E have prices 16, 16, 32, 4, and 12, respectively, for a total price of 80.

The second example above (full of type X and O plants) would have a total price of 436.

Here's a map that includes an E-shaped region full of type E plants:

EEEEE
EXXXX
EEEEE
EXXXX
EEEEE
The E-shaped region has an area of 17 and 12 sides for a price of 204. Including the two regions full of type X plants, this map has a total price of 236.

This map has a total price of 368:

AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA
It includes two regions full of type B plants (each with 4 sides) and a single region full of type A plants (with 4 sides on the outside and 8 more sides on the inside, a total of 12 sides). Be especially careful when counting the fence around regions like the one full of type A plants; in particular, each section of fence has an in-side and an out-side, so the fence does not connect across the middle of the region (where the two B regions touch diagonally). (The Elves would have used the Möbius Fencing Company instead, but their contract terms were too one-sided.)

The larger example from before now has the following updated prices:

A region of R plants with price 12 * 10 = 120.
A region of I plants with price 4 * 4 = 16.
A region of C plants with price 14 * 22 = 308.
A region of F plants with price 10 * 12 = 120.
A region of V plants with price 13 * 10 = 130.
A region of J plants with price 11 * 12 = 132.
A region of C plants with price 1 * 4 = 4.
A region of E plants with price 13 * 8 = 104.
A region of I plants with price 14 * 16 = 224.
A region of M plants with price 5 * 6 = 30.
A region of S plants with price 3 * 6 = 18.
Adding these together produces its new total price of 1206.

What is the new total price of fencing all regions on your map?
'''

import heapq

def inp(fn):
    with open(fn, 'r') as f:
        lines = f.readlines()
    return [l.rstrip() for l in lines]

def first_notvisited(visited):
    for y in range(len(visited)):
        for x in range(len(visited[0])):
            if not visited[y][x]:
                return (x, y)
    return None

def normalize(p1, p2):
    '''return x1,y1 = left top

    >>> normalize((0, 0), (0, 1))
    (0, 0, 0, 1)

    >>> normalize((0, 1), (0, 0))
    (0, 0, 0, 1)

    >>> normalize((1, 1), (1, 0))
    (1, 0, 1, 1)

    >>> normalize((1, 0), (1, 1))
    (1, 0, 1, 1)
    '''
    x1, y1 = p1
    x2, y2 = p2
    if x1 == x2:
        assert y1 != y2, f"{x1}, {y1}, {x2}, {y2}"
        if y1 > y2:
            y1, y2 = y2, y1
    elif y1 == y2:
        assert x1 != x2, f"{x1}, {y1}, {x2}, {y2}"
        if x1 > x2:
            x1, x2 = x2, x1
    else: # must be either H or V; diagonal is err
        assert False, f"{x1}, {y1}, {x2}, {y2}"
    return x1, y1, x2, y2

dpoint = 10 # support self-intersection via small shift inside the cell
shift = 1

# ^>v<
dxdy = [(0, -1), (1, 0), (0, 1), (-1, 0)]
def detect(start, field, visited):
    area, perimeter = 0, 0
    perimeter_segments = set() # x1, y1, x2, y2
    shape = set()
    pushed = set()
    ix, iy = start
    q = []
    heapq.heappush(q, (0, ix, iy))
    pushed.add((ix, iy))
    while len(q) > 0:
        distance, x, y = heapq.heappop(q)
        if visited[y][x]:
            print('====', x, y)
        assert not visited[y][x]
        visited[y][x] = True
        shape.add((x, y))
        perimeter_candidates = [ # borders of this cell (x, y)
            ((x * dpoint, y * dpoint + 1), ((x+1) * dpoint, y * dpoint + shift)), # ^
            (((x+1)* dpoint - shift, y * dpoint), ((x+1)* dpoint - shift, (y+1)* dpoint)), # >
            (((x+1)* dpoint, (y+1)* dpoint - shift), (x* dpoint, (y+1)* dpoint - shift)), # v
            ((x * dpoint + shift, (y+1)* dpoint), (x * dpoint + shift, y * dpoint)) # <
        ]
        area += 1
        candidates = [(x + dx, y + dy) for dx, dy in dxdy]
        for k in range(len(candidates)):
            cx, cy = candidates[k]
            p1, p2 = perimeter_candidates[k]
            if 0 <= cx < len(field[0]) and 0 <= cy < len(field): # if valid
                if visited[cy][cx]:
                    if (cx, cy) in shape:
                        pass # this shape perimeter counted already
                    else: # another shape
                        perimeter += 1
                        perimeter_segments.add(normalize(p1, p2))
                else:
                    if field[y][x] == field[cy][cx]: # this shape continues
                        if (cx, cy) not in pushed:
                            heapq.heappush(q, (distance + 1, cx, cy))
                            pushed.add((cx, cy))
                    else: # another shape
                        perimeter += 1
                        perimeter_segments.add(normalize(p1, p2))
            else: # not valid: field boundary
                perimeter += 1
                perimeter_segments.add(normalize(p1, p2))

    return area, perimeter, perimeter_segments, shape

def count_lines(segments): # one shape, multiple separate contours
    lines = []
    while len(segments) > 0:
        curr = segments.pop()
        curr_line = set()
        curr_line.add(curr)
        x1, y1, x2, y2 = curr
        if x1 == x2: # V
            assert y1 != y2, f"{x1}, {y1}, {x2}, {y2}"
            up = (x1, y1 - dpoint, x1, y1)
            while up in segments:
                curr_line.add(up)
                segments.remove(up)
                up = (up[0], up[1] - dpoint, up[0], up[1])
            down = (x2, y2, x2, y2 + dpoint)
            while down in segments:
                curr_line.add(down)
                segments.remove(down)
                down = (down[2], down[3], down[2], down[3] + dpoint)
            lines.append(curr_line)
        elif y1 == y2: # H
            assert x1 != x2, f"{x1}, {y1}, {x2}, {y2}"
            left = (x1 - dpoint, y1, x1, y1)
            while left in segments:
                curr_line.add(left)
                segments.remove(left)
                left = (left[0] - dpoint, left[1], left[0], left[1])
            right = (x2, y2, x2 + dpoint, y2)
            while right in segments:
                curr_line.add(right)
                segments.remove(right)
                right = (right[2], right[3], right[2] + dpoint, right[3])
            lines.append(curr_line)
        else: # must be either H or V; diagonal is err
            assert False, f"{x1}, {y1}, {x2}, {y2}"
    return lines

def price(field):
    visited = [[False for _ in range(len(field[0]))] for _ in range(len(field))]
    start = first_notvisited(visited)
    total = 0
    while start:
        area, perimeter, perimeter_segments, shape = detect(start, field, visited)
        sides = count_lines(perimeter_segments)
        print(area, 'x', len(sides),'=', area * len(sides) )
        total += area * len(sides)
        start = first_notvisited(visited)
    return total

# f1 = inp('input/12-small-02.txt')
# f1 = inp('input/12-small.txt')
f1 = inp('input/12.txt')
p = price(f1)
print('===============================')
print('The answer: ', p)
print('===============================')
