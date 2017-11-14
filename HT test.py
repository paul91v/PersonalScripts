# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 20:26:18 2017

@author: DELL
"""
from random import choice
curr_pop = [[choice(['Girl','Boy'])] for i in range(1000)]
def birth(children):
    if children[-1] == 'Girl':
        children.append(choice(['Boy','Girl']))
    else:
        pass
    return children
    
def has_boy(children):
    return 'Boy' in children
        
def finish(population):
    return all(map(has_boy,population))

year = 0
while not finish(curr_pop):
    curr_pop = list(map(birth, curr_pop))
    boys_count = len(list(filter(has_boy, curr_pop)))
    girls_count = sum([children.count('Girl') for children in curr_pop])
    print(year, boys_count, girls_count, float(boys_count)/(boys_count + girls_count))
    year+=1