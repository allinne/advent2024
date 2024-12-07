#!/usr/bin/python3

# python3 -m doctest -v 07b.py

'''
--- Part Two ---

The engineers seem concerned; the total calibration result you gave them is nowhere close to being within safety tolerances. Just then, you spot your mistake: some well-hidden elephants are holding a third type of operator.

The concatenation operator (||) combines the digits from its left and right inputs into a single number. For example, 12 || 345 would become 12345. All operators are still evaluated left-to-right.

Now, apart from the three equations that could be made true using only addition and multiplication, the above example has three more equations that can be made true by inserting operators:

156: 15 6 can be made true through a single concatenation: 15 || 6 = 156.
7290: 6 8 6 15 can be made true using 6 * 8 || 6 * 15.
192: 17 8 14 can be made true using 17 || 8 + 14.
Adding up all six test values (the three that could be made before using only + and * plus the new three that can now be made by also using ||) produces the new total calibration result of 11387.

Using your new knowledge of elephant hiding spots, determine which equations could possibly be true. What is their total calibration result?
'''

with open('input/07.txt', 'r') as f:
# with open('input/07-small.txt', 'r') as f:
    lines = f.readlines()
lines = [l.rstrip() for l in lines]

def union(a, b):
    '''
    >>> union(15, 6)
    156
    '''
    return int(str(a) + str(b))

def permute(nums, cache):
    res = set()
    if len(nums) == 1:
        res.add(nums[0])
    else:
        left = nums[:-1]
        last = nums[-1]
        left_str = ','.join([str(i) for i in left])
        if left_str in cache:
            nested = cache[left]
        else:
            nested = permute(left, cache)
            cache[left_str] = nested
        for v in nested:
            res.add(v + last)
            res.add(v * last)
            res.add(union(v, last))
    return res

total = 0
for s in lines:
    target_str, num_str = s.split(':')
    target = int(target_str)
    nums =[int(ns) for ns in num_str.strip().split()]
    if len(nums) == 1:
        if nums[0] == target:
            total += target
    else:
        left = nums[:-1]
        last = nums[-1]
        cache = dict()
        nested = permute(left, cache)
        for v in nested:
            if v + last == target or v * last == target or union(v, last) == target:
                total += target
                break

print('===============================')
print('The answer: ', total)
print('===============================')
