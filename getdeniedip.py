#!/usr/bin/python
"""
Reads Denyhosts denied IP list and returns details of each IP.
Library 'requests' is not standard. "pip install requests" if necessary.
"""
import time
import requests
from os.path import expanduser

def cmonth(month):
    # Returns the monthnumber for the three letter representation
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

def checkip(ip):
    # returns csv formatted line of textinfo about IP as specified in http://ip-api.com/docs/api:csv
    site = "http://ip-api.com/csv/"
    r = requests.get(site+ip)
    return r.text


# Starting program. Skip first 20 lines (junk) and then continue.
lineno = 1
home = expanduser("~")
destfile = open(home+'/result_log.csv', 'w')
source = open('/etc/hosts.deny', 'r')

for i in xrange(20):
    source.next()

for line in source:
    if line[:1] == '#'
        if lineno % 250 == 0:
            print 'Pausing for a minute. Max 250 lookups per minute.'
            time.sleep(60)

        weekday     = line[13:16]
        month       = line[17:20]
        monthno     = cmonth(month)
        daymonth    = line[21:23].replace(' ','0')
        time        = line[24:32]
        year        = line[33:37]
        ip          = line[46:].rstrip('\r\n')

        print '{}: IP {}'.format(lineno,ip)
        lineinfo = '{},{}-{}-{},{},{},'.format(weekday,year,monthno,daymonth,time,ip)
        result = checkip(ip)

        if result[:4] == 'fail':
            print 'Error code received. Aborting.'
            break
        else:
            destfile.write(result + lineinfo + '\n')
            lineno += 1
