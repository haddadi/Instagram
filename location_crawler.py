#!/usr/bin/python

import httplib2
import os
import sys
from collections import defaultdict
import urllib2
import re
import time
from time import sleep
import argparse
from instagram import client, subscriptions
from instagram.client import InstagramAPI
from instagram import client, bind
import random


dataFile = open('xaa', 'r')

access_token = "XXXXXXX"

redirect_uri = "http://www.eecs.qmul.ac.uk/~hamed/public/Hamed.html"
api = InstagramAPI(access_token=access_token)


i=0

for line in dataFile.readlines():
    i +=1;
    print "Line: ",i
    #    print line,
    words = line.split()
    #print words
    parts = line.split("\n")
    #print ('%s', parts[1]);
    str1 = ''.join(words)
    location_id=str1
    filepreamble="output/November2014/location_"
    filepostamble=".txt"
    outputfilename=filepreamble+location_id+filepostamble
    outputfile= open(outputfilename, 'w')
    string1="curl https://api.instagram.com/v1/locations/"
    string2="/media/recent?access_token=XXXXXXX"
    # print location_id
    cmd=string1+location_id+string2
    #os.system('curl "https://api.instagram.com/v1/locations/search?access_token=XXXXXXX&foursquare_v2_id="+location_id ')
    time.sleep(1)
    

    try:
        recent_media, next = api.location_recent_media(location_id=location_id)
    except bind.InstagramAPIError, ie:
        if ie.status_code == 400:
            print "protected account (400) APINotAllowedError-you cannot view this resource"
            continue
        elif ie.status_code == 503:
            # this should not happen, but Instagram returns this message no matter what x_ratelimit_remaining is.
            print "rate limit (503) Rate limited-Your client is making too many request per second"
            time.sleep(10)
            continue
        else:
            print ie
            time.sleep(30)
        continue
    except bind.InstagramClientError, ice:
        if ice.status_code == 404:
            print "instagram.bind.InstagramClientError: (404) Unable to parse response, not valid JSON."
            # no idea why this happens.
            time.sleep(10)
            continue
        elif ice.status_code == 502:
            print "instagram.bind.InstagramClientError: (502) Unable to parse response, not valid JSON."
            time.sleep(10)
            continue
        else:
            print ice
            time.sleep(30)
            continue
    print  api.x_ratelimit_remaining, "requests remained"


    # recent_media, next = api.location_recent_media(location_id=location_id)
    # print  api.x_ratelimit_remaining, "requests remained"

    print next
    print "Location:",location_id
    for media in recent_media:
    	print >> outputfile, media.images['standard_resolution'].url
    	print >> outputfile, media.user
	print >> outputfile, media.location
        if  hasattr(media,'tags'):
        	print >> outputfile, media.tags
        else :
                print >> outputfile, "NO TAGS"
        if media.caption is not 'null':
        	print >> outputfile, media.caption
        else :
        	print >> outputfile, "NO CAPTION"
        if media.comments is not 'null':
        	print >> outputfile, media.comments
        else :
        	print >> outputfile, "NO COMMENTS"
        print >> outputfile, "CRAWLCOMMENTS:",media.comment_count
       	if media.likes is not 'null':
        	print >>  outputfile, media.likes
        else :
        	print >> outputfile, "NO LIKES"
        print >> outputfile, "CRAWLLIKES:", media.like_count#	print "here:", dir(media)
#	sys.exit()
    while next:
        time.sleep(1)

        try:
            recent_media, next = api.location_recent_media(location_id=location_id, with_next_url=next)
        except bind.InstagramAPIError, ie:
            if ie.status_code == 400:
                print "protected account (400) APINotAllowedError-you cannot view this resource"
                continue
            elif ie.status_code == 503:
                # this should not happen, but Instagram returns this message no matter what x_ratelimit_remaining is.
                print "rate limit (503) Rate limited-Your client is making too many request per second"
                time.sleep(10)
                continue
            else:
                print ie
                time.sleep(30)
            continue
        except bind.InstagramClientError, ice:
            if ice.status_code == 404:
                print "instagram.bind.InstagramClientError: (404) Unable to parse response, not valid JSON."
                # no idea why this happens.
                time.sleep(10)
                continue
            elif ice.status_code == 502:
                print "instagram.bind.InstagramClientError: (502) Unable to parse response, not valid JSON."
                time.sleep(10)
                continue
            else:
                print ice
                time.sleep(30)
                continue
        print  api.x_ratelimit_remaining, "requests remained"


#	print next
 #   	print "Location:",location_id
        for media in recent_media:
            print >> outputfile, media.images['standard_resolution'].url
            print >> outputfile, media.user
            print >> outputfile, media.location
            if  hasattr(media,'tags'):
                print >> outputfile, media.tags
            else :
                print >> outputfile, "NO TAGS"
            if media.caption is not 'null':
                print >> outputfile, media.caption
            else :
                print >> outputfile, "NO CAPTION"
            if media.comments is not 'null':
                print >> outputfile, media.comments
            else :
                print >> outputfile, "NO COMMENTS"
            print >> outputfile, "CRAWLCOMMENTS:",media.comment_count
            if media.likes is not 'null':
                print >>  outputfile, media.likes
            else :
                print >> outputfile, "NO LIKES"
            print >> outputfile, "CRAWLLIKES:", media.like_count

#    content = "<h2>Location Recent Media</h2>"

 #   try:
  #      api = client.InstagramAPI(access_token=access_token)
   #     recent_media, next = api.location_recent_media(location_id=str1)
    #    photos = []
     #   for media in recent_media:d
      #      photos.append('<img src="%s"/>' % media.get_standard_resolution_url())
#	    print media.images['standard_resolution'].url        
 #   except Exception, e:
  #      print e              
  #  return "%s %s <br/>Remaining API Calls = %s/%s" % (get_nav(),content,api.x_ratelimit_remaining,api.x_ratelimit)



#        print next
#	string1="curl "
#	string2=next
#	newcmd=string1+string2
#	print newcmd
#	os.system(newcmd)
os.system('echo done')
	#recent_media, next = api.location_recent_media(with_next_url=next)
    	#for media in recent_media:
       # 	print media.images['standard_resolution'].url
 

#	for media in recent_media:
#    recent_media, next = api.location_recent_media(location_id=location_id)
#    photos = []
#    for media in recent_media:
#    	photos.append('<img src="%s"/>' % media.get_standard_resolution_url())
#        print media.images['standard_resolution'].url




#    api = client.InstagramAPI(access_token=access_token)
#    user_follows, next = api.user_follows('10')
#    users = []
#    for user in user_follows:
#    	users.append('%s , %s' % (user.id,user.username))
#    	print user.id,user.username
#    while next:
#    	user_follows, next = api.user_follows(with_next_url=next)
#    	for user in user_follows:
#    		users.append('<li><img src="%s">%s</li>' % (user.profile_picture,user.username))
#    		print user.id,user.username

dataFile.close()
outputfile.close()
