#!/usr/bin/python3

# python3 -m doctest -v 03b.py

'''
As you scan through the corrupted memory, you notice that some of the conditional statements are also still intact. If you handle some of the uncorrupted conditional statements in the program, you might be able to get an even more accurate result.

There are two new instructions you'll need to handle:

The do() instruction enables future mul instructions.
The don't() instruction disables future mul instructions.
Only the most recent do() or don't() instruction applies. At the beginning of the program, mul instructions are enabled.

For example:

xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))
This corrupted memory is similar to the example from before, but this time the mul(5,5) and mul(11,8) instructions are disabled because there is a don't() instruction before them. The other mul instructions function normally, including the one at the end that gets re-enabled by a do() instruction.

This time, the sum of the results is 48 (2*4 + 8*5).

Handle the new instructions; what do you get if you add up all of the results of just the enabled multiplications?
'''

import re
import sys

with open('input/03.txt', 'r') as f:
# with open('input/03b-small.txt', 'r') as f:
    lines = f.readlines()
lines = [l.rstrip() for l in lines]
l2 = "".join(lines)

def extract_xy(line):
    '''
    >>> extract_xy('xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))')
    [[2, 4], [5, 5], [11, 8], [8, 5]]

    >>> extract_xy("what()(!what(),^$mul(929,706)**]+mul(518,107)from()@@!when()where()#] mul(353,511)<who()from()")
    [[929, 706], [518, 107], [353, 511]]

    >>> extract_xy("~%when()mul(318,660)from()when() why():$-[mul(589,949)@&do()?from()mul(455,593)${!*<~*why()#mul(371,828)where()%({ +%$mul(318,225):where()#-?#%mul(816,5)mul(363,524)mul(580,821)/where()what()*{where();mul(223];mul(830,758)~^ why()/?,>why()mul(787,428)( --'who()what()$~mul(314,163)[what()/*~<(</-mul(602,163)@!when()]mul(997,438)<>?#?[ &select())mul(746,865)mul(101,592))}mul(133,751),;',from()mul(226%how()select()/{$!#select(553,217)do()%}mul(538,699))~when()$?* (what()}mul(755,507)+from()who()who()]how(){--[mul(483,410):'  -do()where()$}mul(33,473)mul(835,106)$ {)mul(790,297)how()*where()select()where()*,mul(739,441)mul(561,91)]what()[select()%;what(){mul(601,44where()'):where()(/}<+;mul(956,550)}when()[mul(326,936)<where()~@-mul(238,48)/when()'what()'when()mul(331,847)where()'?")
    [[318, 660], [589, 949], [455, 593], [371, 828], [318, 225], [816, 5], [363, 524], [580, 821], [830, 758], [787, 428], [314, 163], [602, 163], [997, 438], [746, 865], [101, 592], [133, 751], [538, 699], [755, 507], [483, 410], [33, 473], [835, 106], [790, 297], [739, 441], [561, 91], [956, 550], [326, 936], [238, 48], [331, 847]]
    '''
    groups = re.findall('(mul\((\d{1,3}),(\d{1,3})\))', line)  # [('mul(2,4)', '2', '4'), ...
    pairs = [ [int(f[1]), int(f[2])] for f in groups] # [[2, 4], ...
    return pairs

def multiply(xy_list):
    '''
    >>> multiply([[2, 4], [5, 5], [11, 8], [8, 5]])
    161

    >>> multiply([[2, 4], [8, 5]])
    48

    >>> multiply([[929, 706], [518, 107], [353, 511]])
    891683
    '''
    total = 0
    for x, y in xy_list:
        total += x * y
    return total

def enabled_parts(l):
    '''
    >>> enabled_parts("xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))")
    ['xmul(2,4)&mul[3,7]!^', '?mul(8,5))']

    >>> enabled_parts("12mul(9,2)do()Www")
    ['12mul(9,2)do()Www']

    >>> enabled_parts("12mul(9,2)don't()Www")
    ['12mul(9,2)']

    >>> enabled_parts("kkkdon't()Wwwdo()sdmul(2,3)sf")
    ['kkk', 'sdmul(2,3)sf']
    '''
    do = True
    pos = 0
    parts = []
    while pos < len(l):
        if do:
            new_pos = l.find("don't()", pos)
            if new_pos > -1:
                parts.append(l[pos:new_pos])
                pos = new_pos + len("don't()")
                do = False
            else: # dont is not found till end
                parts.append(l[pos:])
                pos = len(l)
        else:
            new_pos = l.find("do()", pos)
            if new_pos > -1:
                do = True
                pos = new_pos + len("do()")
            else: # dont till the end
                pos = len(l)
    return parts

total = 0
parts = enabled_parts(l2)
for p in parts:
    xy_list = extract_xy(p)
    total += multiply(xy_list)

print('===============================')
print('The answer: ' + str(total)) # 84893551
print('===============================')
