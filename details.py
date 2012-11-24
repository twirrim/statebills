#!/usr/bin/env python

import csv
import time
import datetime
import sys, os
import urllib
import re
import nltk
from git import *

repo = Repo("./bills")
assert repo.bare == False

urlname = re.compile("(\A[A-Z]+[0-9]+_)")

with open('order.csv','rb') as csvfile:
    read = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in read:
        filetime = datetime.datetime.strptime(row[0],"%A, %B %d, %Y  %I:%M %p")
        url = "http://www.capitol.hawaii.gov%s" % (row[2])
        bill = urlname.match(row[2].rpartition('/')[2]).group(0)+".txt"
        while True:
            try:
                print "Fetching url %s" % (url)
                html = urllib.urlopen(url).read()
                time.sleep(1)
            except:
                print "Fetch failed, pausing then retrying"
                time.sleep(30)
                continue
            else:
                text = nltk.clean_html(html)
                destination = "./bills/%s" % bill
                f = open(destination,'w')
                f.write(text)
                f.close()
                repo.git.add(bill)
                repo.git.commit(m=row[0],date=filetime)
                break
