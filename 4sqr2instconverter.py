#!/usr/bin/python

import httplib2
import os
import sys
import urllib2
import re
import time
import subprocess
from time import sleep


dataFile = open('4sq_USA_food_location_ids.txt', 'r')
outputfile = open ('4sq2inst_mapped_with_4sq_id_at_end.txt', 'w')

for line in dataFile:
    location_id=line
    string="curl https://api.instagram.com/v1/locations/search?access_token=XXXXXXX\&foursquare_v2_id="
    #    print location_id
    cmd=string+location_id
    output = subprocess.check_output(cmd, shell=True)
    #    os.system(cmd)
    print >> outputfile, output+' '+line,
    #os.system('echo')
#os.system('curl "https://api.instagram.com/v1/locations/search?access_token=XXXXXXX&foursquare_v2_id="+location_id ')
#    time.sleep(1)
dataFile.close()
