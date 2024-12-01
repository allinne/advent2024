#!/usr/bin/python3

# python3 -m doctest -v 01b.py

'''
This time, you'll need to figure out exactly how often each number from the left list appears in the right list. Calculate a total similarity score by adding up each number in the left list after multiplying it by the number of times that number appears in the right list.

Here are the same example lists again:

3   4
4   3
2   5
1   3
3   9
3   3
For these example lists, here is the process of finding the similarity score:

The first number in the left list is 3. It appears in the right list three times, so the similarity score increases by 3 * 3 = 9.
The second number in the left list is 4. It appears in the right list once, so the similarity score increases by 4 * 1 = 4.
The third number in the left list is 2. It does not appear in the right list, so the similarity score does not increase (2 * 0 = 0).
The fourth number, 1, also does not appear in the right list.
The fifth number, 3, appears in the right list three times; the similarity score increases by 9.
The last number, 3, appears in the right list three times; the similarity score again increases by 9.
So, for these example lists, the similarity score at the end of this process is 31 (9 + 4 + 0 + 0 + 9 + 9).

Once again consider your left and right lists. What is their similarity score?
'''

# with open('input/01-small.txt', 'r') as f:
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

def read_lists(lines_array):
    '''
    >>> read_lists(['15259   96330', '81076   52363'])
    ([15259, 81076], [96330, 52363])
    '''

    left_column = []
    right_column = []
    for l in lines_array:
        parsed_line = parse_line(l)
        left_column.append(parsed_line[0])
        right_column.append(parsed_line[1])

    return (left_column, right_column)

arr1, arr2 = read_lists(lines)
v2_count = {}
for v in arr2:
    count = v2_count[v] if v in v2_count else 0
    new_count = count + 1
    v2_count[v] = new_count

total = 0
for v in arr1:
    count = v2_count[v] if v in v2_count else 0
    total += v * count

print('===============================')
print('The answer: ' + str(total))
print('===============================')
