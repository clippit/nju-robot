#!/usr/bin/python
# -*- coding:utf-8 -*-

import urllib2, urllib
import oauth

# User ID: 47795365
CONSUMER_KEY = oauth.OAuthConsumer('0eea6ff9bd3123bf2cbf4fed37936b3d', '3029eaa0862b9597')
TOKEN = oauth.OAuthToken('374f0cd8e44f734ca5ed268aacee59e4', '1abca0f7e2d8157e')
URL_RECOMMENDATIONS = 'http://api.douban.com/recommendations'

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
	print postdata.encode('UTF-8')
	header = get_request_header(URL_RECOMMENDATIONS, 'POST')
	req = urllib2.Request(URL_RECOMMENDATIONS, postdata.encode('UTF-8'), header)
	req.add_header('Content-Type', 'application/atom+xml')
	req.add_header('User-Agent', '')
	response = urllib2.urlopen(req)