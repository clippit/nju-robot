#!/usr/bin/python
# -*- coding:utf-8 -*-

import urllib2, urllib, datetime
import oauth
import config

# User ID: 47795365
CONSUMER_KEY = oauth.OAuthConsumer(config.DOUBAN_OAUTH_CONSUMER_KEY, config.DOUBAN_OAUTH_CONSUMER_TOKEN)
TOKEN = oauth.OAuthToken(config.DOUBAN_OAUTH_TOKEN_KEY, config.DOUBAN_OAUTH_TOKEN_TOKEN)
URL_RECOMMENDATIONS = 'http://api.douban.com/recommendations'
URL_EVENTS = 'http://api.douban.com/events'

def get_request_header(url, method, param=None):
	oauth_request = oauth.OAuthRequest.from_consumer_and_token(CONSUMER_KEY, TOKEN, http_method=method, http_url=url, parameters=param)
	oauth_request.sign_request(oauth.OAuthSignatureMethod_HMAC_SHA1(), CONSUMER_KEY, TOKEN)
	return oauth_request.to_header()

def add_recommendation(title, excerpt, link):
	postdata = u'''<?xml version="1.0" encoding="UTF-8"?>
<entry xmlns="http://www.w3.org/2005/Atom"
        xmlns:gd="http://schemas.google.com/g/2005"
        xmlns:opensearch="http://a9.com/-/spec/opensearchrss/1.0/"
        xmlns:db="http://www.douban.com/xmlns/">
        <title>%s</title>
        <db:attribute name="comment">%s</db:attribute>
        <link href="%s" rel="related" />
</entry>''' % (title, excerpt, link)
	#print postdata.encode('UTF-8')
	header = get_request_header(URL_RECOMMENDATIONS, 'POST')
	req = urllib2.Request(URL_RECOMMENDATIONS, postdata.encode('UTF-8'), header)
	req.add_header('Content-Type', 'application/atom+xml')
	req.add_header('User-Agent', '')
	response = urllib2.urlopen(req)

def add_events(title, content, time, place):
	two_hours = datetime.timedelta(hours=2)
	postdata = u'''<?xml version="1.0" encoding="UTF-8"?>
<entry xmlns="http://www.w3.org/2005/Atom" xmlns:db="http://www.douban.com/xmlns/" xmlns:gd="http://schemas.google.com/g/2005" xmlns:opensearch="http://a9.com/-/spec/opensearchrss/1.0/">
<title>%s</title>
<category scheme="http://www.douban.com/2010#kind" term="http://www.douban.com/2010#event.salon"/>
<content>%s</content>

<db:attribute name="invite_only">no</db:attribute>
<db:attribute name="can_invite">yes</db:attribute>
<gd:when endTime="%s" startTime="%s"/>
<gd:where valueString="%s"/>
</entry>''' % (title, content, (time+two_hours).strftime('%Y-%m-%dT%H:%M:%S+08:00'), time.strftime('%Y-%m-%dT%H:%M:%S+08:00'), place)
	#print postdata.encode('UTF-8')
	header = get_request_header(URL_EVENTS, 'POST')
	req = urllib2.Request(URL_EVENTS, postdata.encode('UTF-8'), header)
	req.add_header('Content-Type', 'application/atom+xml')
	req.add_header('User-Agent', '')
	response = urllib2.urlopen(req)