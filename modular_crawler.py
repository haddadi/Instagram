#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from collections import defaultdict
import string
import operator
from instagram import client, bind
import os
from subprocess import call, check_output
import time
import random



reload(sys)
sys.setdefaultencoding("utf-8")

def save(NUMBER_OF_CRAWLERS, THIS_CRAWLER, recent):
    with open("final_state_%d_%d.txt" % (THIS_CRAWLER, NUMBER_OF_CRAWLERS), "w") as fo:
        fo.write("%d\n" % recent)

def load(NUMBER_OF_CRAWLERS, THIS_CRAWLER):
    if not os.path.exists("final_state_%d_%d.txt" % (THIS_CRAWLER, NUMBER_OF_CRAWLERS)):
        return 0

    with open("final_state_%d_%d.txt" % (THIS_CRAWLER, NUMBER_OF_CRAWLERS)) as fi:
        return int(fi.read())

def initialization(NUMBER_OF_CRAWLERS, THIS_CRAWLER):
    raw_tokens = [token.strip() for token in open("tokens.txt").readlines()]
    tokens = []
    for token_id, token in enumerate(raw_tokens):
        if (token_id % NUMBER_OF_CRAWLERS)+1 == THIS_CRAWLER:
            tokens.append(token)

    return tokens

def check_ratelimit(remaining_requests):
    if remaining_requests < 30:
        print "remaining requests are ", remaining_requests, "; sleep 30 seconds"
        time.sleep(30)

def crawl_ego_network(NUMBER_OF_CRAWLERS, THIS_CRAWLER, token):
    time.sleep(1)
    next_pos = load(NUMBER_OF_CRAWLERS, THIS_CRAWLER) + 1
    output = "result/network_%s_%d_%d.txt" % (time.strftime("%Y%m%d"), THIS_CRAWLER, NUMBER_OF_CRAWLERS)

    fo = open(output, "a") 
    while True:
        if next_pos % NUMBER_OF_CRAWLERS != THIS_CRAWLER:
            next_pos += 1
        else:
            break

    target_id = str(next_pos)
    print "crawling [%s]" % target_id

    api = client.InstagramAPI(access_token=token)            
    try:
        user_followees, next_url = api.user_follows(target_id, count=100)
    except bind.InstagramAPIError, ie:
        if ie.status_code == 400:
            print "protected account (400) APINotAllowedError-you cannot view this resource"      
        else:
            print ie
        time.sleep(3)
        save(NUMBER_OF_CRAWLERS, THIS_CRAWLER, next_pos)
        return
    except bind.InstagramClientError, ice:
        if ice.status_code == 404:
            print "instagram.bind.InstagramClientError: (404) Unable to parse response, not valid JSON."
            # no idea why this happens.
        elif ice.status_code == 502:
            print "instagram.bind.InstagramClientError: (502) Unable to parse response, not valid JSON."
        else:
            print ice
        time.sleep(3)
        save(NUMBER_OF_CRAWLERS, THIS_CRAWLER, next_pos)
        return

    print len(user_followees), "followees of", target_id, "are collected.. ", api.x_ratelimit_remaining, "requests remained"
    check_ratelimit(api.x_ratelimit_remaining)
   
    for user in user_followees:
        # do something
        fo.write("%s\t%s\n" % (target_id, user.id))

    while next_url:
        try:
            user_followees, next_url = api.user_follows(with_next_url = next_url, count=100)
        except bind.InstagramAPIError, ie:
            if ie.status_code == 503:
                # this should not happen, but Instagram returns this message no matter what x_ratelimit_remaining is.
                print "rate limit (503) Rate limited-Your client is making too many request per second"
            else:
                print ie
                print ie.status_code
                print type(ie.status_code)

            time.sleep(3)
            save(NUMBER_OF_CRAWLERS, THIS_CRAWLER, next_pos)
            return    
        except bind.InstagramClientError, ice:
            if ice.status_code == 404:
                print "instagram.bind.InstagramClientError: (404) Unable to parse response, not valid JSON."
                # no idea why this happens.

            elif ice.status_code == 502:
                print "instagram.bind.InstagramClientError: (502) Unable to parse response, not valid JSON."

            else:
                print ice
            time.sleep(3)
            save(NUMBER_OF_CRAWLERS, THIS_CRAWLER, next_pos)
            return     

        print len(user_followees), "followees of", target_id, "are collected.. ", api.x_ratelimit_remaining, "requests remained"
        check_ratelimit(api.x_ratelimit_remaining)
        for user in user_followees:
            # do something
            fo.write("%s\t%s\n" % (target_id, user.id))

    try:
        user_followers, next_url = api.user_followed_by(target_id, count=100)
    except bind.InstagramAPIError, ie:
        if ie.status_code == 400:
            print "protected account (400) APINotAllowedError-you cannot view this resource"      
        else:
            print ie
        time.sleep(3)
        save(NUMBER_OF_CRAWLERS, THIS_CRAWLER, next_pos)
        return
    except bind.InstagramClientError, ice:
        if ice.status_code == 404:
            print "instagram.bind.InstagramClientError: (404) Unable to parse response, not valid JSON."
            # no idea why this happens.
        elif ice.status_code == 502:
            print "instagram.bind.InstagramClientError: (502) Unable to parse response, not valid JSON."
        else:
            print ice
        time.sleep(3)
        save(NUMBER_OF_CRAWLERS, THIS_CRAWLER, next_pos)
        return

    print len(user_followers), "followers of", target_id, "are collected.. ", api.x_ratelimit_remaining, "requests remained"
    check_ratelimit(api.x_ratelimit_remaining)
   
    for user in user_followers:
        # do something
        fo.write("%s\t%s\n" % (user.id, target_id))

    while next_url:
        try:
            user_followers, next_url = api.user_followed_by(with_next_url = next_url, count=100)
        except bind.InstagramAPIError, ie:
            if ie.status_code == 503:
                # this should not happen, but Instagram returns this message no matter what x_ratelimit_remaining is.
                print "rate limit (503) Rate limited-Your client is making too many request per second"
            else:
                print ie
                print ie.status_code
                print type(ie.status_code)
            time.sleep(3)
            save(NUMBER_OF_CRAWLERS, THIS_CRAWLER, next_pos)
            return              
        except bind.InstagramClientError, ice:
            if ice.status_code == 404:
                print "instagram.bind.InstagramClientError: (404) Unable to parse response, not valid JSON."
                # no idea why this happens.

            elif ice.status_code == 502:
                print "instagram.bind.InstagramClientError: (502) Unable to parse response, not valid JSON."

            else:
                print ice
            time.sleep(3)
            save(NUMBER_OF_CRAWLERS, THIS_CRAWLER, next_pos)
            return              

        print len(user_followers), "followers of", target_id, "are collected.. ", api.x_ratelimit_remaining, "requests remained"
        check_ratelimit(api.x_ratelimit_remaining)
        for user in user_followers:
            # do something
            fo.write("%s\t%s\n" % (user.id, target_id))

    save(NUMBER_OF_CRAWLERS, THIS_CRAWLER, next_pos)
    fo.close()

    # if api.x_ratelimit_remaining < 30:
    #     print "some breaks.."
    #     time.sleep(5)  

def ordinal(n):
    return "%d%s" % (n,"tsnrhtdd"[(n/10%10!=1)*(n%10<4)*n%10::4])

if __name__ == "__main__":
    if len(sys.argv) == 3:
        THIS_CRAWLER = int(sys.argv[1])
        NUMBER_OF_CRAWLERS = int(sys.argv[2])        

        print "this is the %s crawler among %s." % (ordinal(THIS_CRAWLER), sys.argv[2])

    else:
        print "python crawler.py [THIS_ID] [MAX_ID (from 1)]"
        print "ex) when two distributed crawlers are available,"
        print "$ python crawler.py 1 2"
        sys.exit()
    
    tokens = initialization(NUMBER_OF_CRAWLERS, THIS_CRAWLER)
    print len(tokens), " tokens are available for this crawler"
    print tokens
    if THIS_CRAWLER == NUMBER_OF_CRAWLERS:
        THIS_CRAWLER = 0
    while True:
        for token in tokens:
            crawl_ego_network(NUMBER_OF_CRAWLERS, THIS_CRAWLER, token)
