#!/usr/bin/python3

# python3 -m doctest -v 05b.py

'''
--- Part Two ---

While the Elves get to work printing the correctly-ordered updates, you have a little time to fix the rest of them.

For each of the incorrectly-ordered updates, use the page ordering rules to put the page numbers in the right order. For the above example, here are the three incorrectly-ordered updates and their correct orderings:

75,97,47,61,53 becomes 97,75,47,61,53.
61,13,29 becomes 61,29,13.
97,13,75,29,47 becomes 97,75,47,29,13.
After taking only the incorrectly-ordered updates and ordering them correctly, their middle page numbers are 47, 29, and 47. Adding these together produces 123.

Find the updates which are not in the correct order. What do you get if you add up the middle page numbers after correctly ordering just those updates?
'''

import sys

with open('input/05.txt', 'r') as f:
# with open('input/05-small.txt', 'r') as f:
    lines = f.readlines()
lines = [l.rstrip() for l in lines]

rules = []
k = 0
while k < len(lines) and lines[k]:
    ss = lines[k].split('|')
    vv = [int(s) for s in ss]
    rules.append(vv)
    k += 1
k += 1 # update

first_second = {}
second_first = {}
for first, second in rules:
    if first in first_second:
        first_second[first].add(second)
    else:
        first_second[first] = {second}

    if second in second_first:
        second_first[second].add(first)
    else:
        second_first[second] = {first}

def is_after(curr, preceeding):
    b = True
    if len(preceeding) > 0:
        for p in preceeding:
            if p in first_second:
                if curr in first_second[p]:
                    pass # OK: v must be after p, which preceeds
                else:
                    pass # not found p > v
            else:
                pass # not found p > ???

            # if curr must be before p
            if curr in first_second:
                if p in first_second[curr]:
                    b = False
                    break
    return b

def is_before(curr, following):
    b = True
    if len(following) > 0:
        if curr in first_second:
            must = first_second[curr]
            for a in following:
                if a in must:
                    pass # curr > a
                    pass
                    pass
                else:
                    pass # unknown curr > a
        for a in following:
            if a in first_second:
                if curr in first_second[a]:
                    b = False
                    break
    return b

def is_correct(u):

    # tests depend on first_second, which is from 05-small.txt
    # '''
    # >>> correct([75,47,61,53,29])
    # True
    #
    # >>> correct([97,61,53,29,13])
    # True
    #
    # >>> correct([75,29,13])
    # True
    #
    # >>> correct([75,97,47,61,53])
    # False
    #
    # >>> correct([61,13,29])
    # False
    #
    # >>> correct([97,13,75,29,47])
    # False
    # '''

    b = True
    for k in range(len(u)):
        preceeding = u[:k]
        following = u[k+1:] if k+1 < len(u) else []
        if not is_after(u[k], preceeding):
            b = False
            break
        if not is_before(u[k], following):
            b = False
            break
    return b

def fix(u):

    # tests depend on first_second, which is from 05-small.txt
    # '''
    # >>> fix([75, 97, 47, 61, 53])
    # [97, 75, 47, 61, 53]
    #
    # >>> fix([61,13,29])
    # [61, 29, 13]
    #
    # >>> fix([97,13,75,29,47])
    # [97, 75, 47, 29, 13]
    # '''
    fixed = []
    if len(u) < 2:
        fixed = u
    else:
        a = u[0]
        tail = u[1:]
        tail_sorted = fix(tail)
        b = tail_sorted[0] # the rest is after b
        if a in first_second:
            after_a = first_second[a]
            if b in after_a:  # a before b
                pass # ok, b after a
                fixed = [a] + tail_sorted

        if b in first_second:
            after_b = first_second[b]
            if a in after_b:
                # everything in tail_sorted[1:] is sorted and after b already
                right_to_sort = [a] + tail_sorted[1:]
                # a can be moved further inside right_to_sort
                tail_sorted2 = fix(right_to_sort)
                fixed = [b] + tail_sorted2
    return fixed

total = 0
for u_str in lines[k:]:
    u = [int(s) for s in u_str.split(',')]
    if not is_correct(u):
        f = fix(u)
        if len(u) != len(f):
            print('@@@@@@@@@@@@@@@@@')
            print('Cannot fix', u)
            print('@@@@@@@@@@@@@@@@@')
            sys.exit(34)
        total += f[int(len(f) / 2)]
print('===============================')
print('The answer: ', total)
print('===============================')
