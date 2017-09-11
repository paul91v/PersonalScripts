# -*- coding: utf-8 -*-
"""
Created on Mon Sep 11 13:24:11 2017

@author: paulvannank
"""

import win32evtlog
import datetime as dt
from time import mktime

server = 'ADF-1049' # name of the target computer to get event logs
logtype = 'System'
hand = win32evtlog.OpenEventLog(server,logtype)
flags = win32evtlog.EVENTLOG_BACKWARDS_READ|win32evtlog.EVENTLOG_SEQUENTIAL_READ
total = win32evtlog.GetNumberOfEventLogRecords(hand)

#==============================================================================
# while True:
#     events = win32evtlog.ReadEventLog(hand, flags,0)
#     if events:
#         for event in events:
#             if event.EventID == "7002":
#                 print 'Event Category:', event.EventCategory
#                 print 'Time Generated:', event.TimeGenerated
#                 print 'Source Name:', event.SourceName
#                 print 'Event ID:', event.EventID
#                 print 'Event Type:', event.EventType
#                 data = event.StringInserts
#                 if data:
#                     print 'Event Data:'
#                     for msg in data:
#                         print msg
#                 break
#==============================================================================

def weekdays():
    return [dt.datetime.now().date()-dt.timedelta(days = i) for i in range(dt.datetime.now().weekday()+1)]

flag = 0
i = 0
hand = win32evtlog.OpenEventLog(server,logtype)
while (not flag) and (i<1000):
    events = win32evtlog.ReadEventLog(hand, 9,0)
    i+=1
    for event in events:
        if event.EventID == 7001 and dt.datetime.fromtimestamp(mktime(event.TimeGenerated)).date() in weekdays(dt.datetime.now().date()) :
            print 'Event Category:', event.EventCategory
            print 'Time Generated:', event.TimeGenerated
            print 'Source Name:', event.SourceName
            print 'Event ID:', event.EventID
            print 'Event Type:', event.EventType
            data = event.StringInserts
            flag = 1

