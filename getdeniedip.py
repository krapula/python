#!/usr/bin/python
"""
Reads Denyhosts denied IP list and returns details of each IP.
"""
import time
import requests
from os.path import expanduser

def cmonth(month):
    months = {
            'Jan':'01',
            'Feb':'02',
            'Mar':'03',
            'Apr':'04',
            'May':'05',
            'Jun':'06',
            'Jul':'07',
            'Aug':'08',
            'Sep':'09',
            'Oct':'10',
            'Nov':'11',
            'Dec':'12',
            }
    return months[month]

def cdaymonth(d):
    if len(d) == 1:
        d = '0' + d

    return d

def checkip(ip):
    # returns csv formatted line of textinfo about IP as specified in http://ip-api.com/docs/api:csv
    site = "http://ip-api.com/csv/"
    r = requests.get(site+ip)
    return r.text

def getLineInfo(line):
    info = {
            'weekday':'',
            'month':'',
            'monthno':'',
            'daymonth':'',
            'time':'',
            'year':'',
            'ip':''
            }

    s = line.split()
    info['weekday']     = s[2]
    info['month']       = s[3]
    info['monthno']     = cmonth(s[3])
    info['daymonth']    = cdaymonth(s[4])
    info['time']        = s[5]
    info['year']        = s[6]
    info['ip']          = s[9]

    return info


# Starting program
lineno = 1
home = expanduser("~")
destfile = open(home+'/result_log.csv', 'w')
source = open('/etc/hosts.deny', 'r')

for i in xrange(20):
    source.next()

for line in source:
    if line[:1] == '#':
        if lineno % 250 == 0:
            print 'Pausing for a minute. Max 250 lookups per minute.'
            time.sleep(60)

        info = getLineInfo(line)    

        print '{}: IP {}'.format(lineno, info['ip'])
        lineinfo = '{},{}-{}-{},{},{}'.format(info['weekday'], info['year'], info['monthno'], info['daymonth'], info['time'], info['ip'])
        result = checkip(info['ip'])

        if result[:4] == 'fail':
            print 'Error code received. Aborting.'
            break
        else:
            destfile.write(result + ',' + lineinfo + '\n')
            lineno += 1
