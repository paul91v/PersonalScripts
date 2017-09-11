# -*- coding: utf-8 -*-
"""
Created on Wed Sep 06 10:18:55 2017

@author: paulvannank
"""
import pandas as pd
import datetime as dt


LoginTimes = pd.read_csv('E:\Python Scripts\Personal Scripts\LoginTimes.csv')
LoginTimes = LoginTimes.set_index('Date')
ans = True
while ans:
    d = raw_input("\nEnter the Date for the Entry in DD-MM-YYYY Format: (Enter 'T' for Today) :\n")
    if d=='T':
        d = dt.date.today()
    else:
        try:
            ds = dt.datetime.strptime(d, '%d-%m-%Y').date()
        except ValueError:
            print 'Invalid format for Date'
            continue
    t = raw_input("\nEnter the Time in 'HH:MM AM/PM I/O' format where I/O is In or Out :\n")
    IO = t[-1]
    t = t[:-2]
    try:
        t = dt.datetime.strptime(t, '%I:%M %p').time()
        if IO!='I' and IO!='O':
            raise ValueError
    except ValueError:
        print 'Invalid format for Time'
        continue
    if d in LoginTimes.index:
        print 'in'
        if IO=='I':
            LoginTimes.iloc[d]['In Time'] = t
        elif IO=='O':
            LoginTimes.iloc[d]['Out Time'] = t
    else:
        print 'not in'
        if IO == 'I':
            LoginTimes.loc[ds] = [t,None]
        elif IO=='O':
            LoginTimes.loc[ds] = [None, t]        
    ans = raw_input('\nDo You want to continue? Yes/No :\n')
    if ans == 'Yes':
        ans = True
    else:
        ans = False
LoginTimes.to_csv('E:\Python Scripts\Personal Scripts\LoginTimes.csv')