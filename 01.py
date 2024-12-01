#!/usr/bin/python3

# python3 -m doctest -v 01.py

'''
There's just one problem: by holding the two lists up side by side (your puzzle input), it quickly becomes clear that the lists aren't very similar. Maybe you can help The Historians reconcile their lists?

For example:

3   4
4   3
2   5
1   3
3   9
3   3
Maybe the lists are only off by a small amount! To find out, pair up the numbers and measure how far apart they are. Pair up the smallest number in the left list with the smallest number in the right list, then the second-smallest left number with the second-smallest right number, and so on.

Within each pair, figure out how far apart the two numbers are; you'll need to add up all of those distances. For example, if you pair up a 3 from the left list with a 7 from the right list, the distance apart is 4; if you pair up a 9 with a 3, the distance apart is 6.

In the example list above, the pairs and distances would be as follows:

The smallest number in the left list is 1, and the smallest number in the right list is 3. The distance between them is 2.
The second-smallest number in the left list is 2, and the second-smallest number in the right list is another 3. The distance between them is 1.
The third-smallest number in both lists is 3, so the distance between them is 0.
The next numbers to pair up are 3 and 4, a distance of 1.
The fifth-smallest numbers in each list are 3 and 5, a distance of 2.
Finally, the largest number in the left list is 4, while the largest number in the right list is 9; these are a distance 5 apart.
To find the total distance between the left list and the right list, add up the distances between all of the pairs you found. In the example above, this is 2 + 1 + 0 + 1 + 2 + 5, a total distance of 11!

Your actual left and right lists contain many location IDs. What is the total distance between your lists?
'''

import re

with open('input/01.txt', 'r') as f:
    lines = f.readlines()
lines = [l.rstrip() for l in lines]

def parse_line(line):
    '''
    >>> parse_line('15259   96330')
    (15259, 96330)
    '''

    n1, n2 = [int(s) for s in line.split()]
    return (n1, n2)

def fill_and_sort_arrays(lines_array):
    '''
    >>> fill_and_sort_arrays(['15259   96330', '81076   52363'])
    ([15259, 81076], [52363, 96330])
    '''

    left_column = []
    right_column = []
    for l in lines_array:
        parsed_line = parse_line(l)
        left_column.append(parsed_line[0])
        right_column.append(parsed_line[1])

    return (sorted(left_column), sorted(right_column))

def find_distance(array1, array2):
    '''
    >>> find_distance([2, 5], [3, 5])
    [1, 0]
    '''

    distance_array = []
    for i in range(len(array1)):
        distance_array.append(abs(array1[i] - array2[i]))

    return distance_array

def total_distance(dist_array):
    '''
    >>> total_distance([2, 5, 1, 0, 3])
    11
    '''
    sum = 0
    for i in dist_array:
        sum += i

    return sum


arr1, arr2 = fill_and_sort_arrays(lines)
dist = find_distance(arr1, arr2)
print(total_distance(dist))
