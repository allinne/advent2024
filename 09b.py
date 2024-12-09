#!/usr/bin/python3

# python3 -m doctest -v 09b.py

'''
--- Part Two ---

Upon completion, two things immediately become clear. First, the disk definitely has a lot more contiguous free space, just like the amphipod hoped. Second, the computer is running much more slowly! Maybe introducing all of that file system fragmentation was a bad idea?

The eager amphipod already has a new plan: rather than move individual blocks, he'd like to try compacting the files on his disk by moving whole files instead.

This time, attempt to move whole files to the leftmost span of free space blocks that could fit the file. Attempt to move each file exactly once in order of decreasing file ID number starting with the file with the highest file ID number. If there is no span of free space to the left of a file that is large enough to fit the file, the file does not move.

The first example from above now proceeds differently:

00...111...2...333.44.5555.6666.777.888899
0099.111...2...333.44.5555.6666.777.8888..
0099.1117772...333.44.5555.6666.....8888..
0099.111777244.333....5555.6666.....8888..
00992111777.44.333....5555.6666.....8888..
The process of updating the filesystem checksum is the same; now, this example's checksum would be 2858.

Start over, now compacting the amphipod's hard drive using this new method instead. What is the resulting filesystem checksum?
'''

import sys

with open('input/09.txt', 'r') as f:
# with open('input/09-small.txt', 'r') as f:
    lines = f.readlines()
lines = [l.rstrip() for l in lines]

l = lines[0]
disk = []
available = []
files = []
id = 0
for k in range(len(l)):
    if k%2 == 0:
        files.append([len(disk), int(l[k])])
        for j in range(int(l[k])):
            disk.append(id)
        id += 1
    else:
        space = int(l[k])
        if space > 0:
            available.append([len(disk), space])
            for m in range(space):
                disk.append('.')

for file_id in range(len(files) - 1, -1, -1):
    pos_file, sz = files[file_id]
    dst = -1
    for j in range(len(available)):
        pos, space = available[j]
        if pos >= pos_file:
            break
        if sz <= space:
            dst = j
            break

    if -1 < dst:
        pos, space = available[dst]
        for j in range(sz):
            disk[pos + j] = file_id
            disk[pos_file + j] = '.'
        available[dst] = [pos + sz, space - sz]

def checksum():
    sum = 0
    for k in range(len(disk)):
        if disk[k] != '.':
            sum += k * disk[k]
    return sum

print('===============================')
print('The answer: ', checksum())
print('===============================')
