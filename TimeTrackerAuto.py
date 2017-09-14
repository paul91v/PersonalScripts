# -*- coding: utf-8 -*-
"""
Created on Mon Sep 11 13:24:11 2017

@author: paulvannank
"""

import win32evtlog
import datetime as dt
import pandas as pd
import os

server =  os.environ['COMPUTERNAME']# name of the target computer to get event logs
logtype = 'System'
hand = win32evtlog.OpenEventLog(server,logtype)
flags = win32evtlog.EVENTLOG_BACKWARDS_READ|win32evtlog.EVENTLOG_SEQUENTIAL_READ
total = win32evtlog.GetNumberOfEventLogRecords(hand)

def weekdays():
    return [(dt.datetime.now().date()-dt.timedelta(days = i)).strftime('%m/%d/%y') for i in range(dt.datetime.now().weekday()+1)]

flag = 0
i = 0
times = pd.DataFrame(columns = ['Date','In','Out'])
hand = win32evtlog.OpenEventLog(server,logtype)
while (flag!=2*len(weekdays()) - 1) and (i<1000):
    events = win32evtlog.ReadEventLog(hand, flags, 0)
    i+=1
    for event in events:
        if event.EventID in [7001,7002] and event.TimeGenerated.Format()[:8] in weekdays() :
            if event.TimeGenerated.Format()[:8] in list(times['Date']):
                flag+=1
                if event.EventID == 7001:
                    times.ix[times.index[times.Date == event.TimeGenerated.Format()[:8]][0], 'In'] = event.TimeGenerated.Format()[-8:]
                else:
                    times.ix[times.index[times.Date == event.TimeGenerated.Format()[:8]][0], 'Out'] = event.TimeGenerated.Format()[-8:]
                times.reset_index(drop = True, inplace = True)
            else:
                flag+=1
                if event.EventID == 7001:
                    #print 'hitting Login'
                    temp = pd.DataFrame([[event.TimeGenerated.Format()[:8], event.TimeGenerated.Format()[-8:], None]], columns = ['Date','In','Out'])
                    times = times.append(temp)
                else:
                    temp = pd.DataFrame([[event.TimeGenerated.Format()[:8], None, event.TimeGenerated.Format()[-8:]]], columns = ['Date','In','Out'])
                    times = times.append(temp)
                times.reset_index(drop = True, inplace = True)
            print '\n'
times.ix[times.index[times.Date == weekdays()[0]][0], 'Out'] = dt.datetime.now().time().strftime('%H:%M:%S')
times['WorkTime'] = pd.to_datetime(times['Out'], format = '%H:%M:%S') - pd.to_datetime(times['In'], format = '%H:%M:%S')
total = reduce(lambda x,y :x+y, list(times['WorkTime']))
print times
print '\nSpent Time :',total.days*24+total.seconds//3600,'Hours,', (total.seconds%3600)//60, 'Minutes '
print '\nRemaining Time :', 44 - (total.days*24+total.seconds//3600) + (60 - (total.seconds%3600)//60)//60,'Hours, ',  (60 - (total.seconds%3600)//60)%60, 'Minutes '
