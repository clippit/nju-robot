#!/usr/bin/python
# -*- coding:utf-8 -*-

import urllib2, urllib, base64
#import oauth

# Username: NJUlily
#CONSUMER_KEY = oauth.OAuthConsumer('rs7lclE1VGhHgcWeKCoYsw', 'WzDfqSYV5xmTTbQpsJFKuhVhbBYLxdbmi1Y6slf6k')
#TOKEN = oauth.OAuthToken('224662102-92AHuYAj8t9i66ACWgC5t9eHCCZdN53XNdLj63ko', 'd3BhKIdrvPr09lcuDay49VglHV5wLPESD0GpmyzOj8')
#URL_STATUES_UPDATE = 'http://api.twitter.com/1/statuses/update.json'

#def get_request_header(url, method, param=None):
#	oauth_request = oauth.OAuthRequest.from_consumer_and_token(CONSUMER_KEY, TOKEN, http_method=method, http_url=url, parameters=param)
#	oauth_request.sign_request(oauth.OAuthSignatureMethod_HMAC_SHA1(), CONSUMER_KEY, TOKEN)
#	return oauth_request.to_header()

#def status_update(content):
#	postdata = {'status': content.encode('UTF-8')}
#	header = get_request_header(URL_STATUES_UPDATE, 'POST', postdata)
#	req = urllib2.Request(URL_STATUES_UPDATE, urllib.urlencode(postdata), header)
#	response = urllib2.urlopen(req, timeout=20)
	#return response.read()

def status_update(content):
	''' Use dayanjia.com for a proxy'''
	postdata = {'status': base64.b64encode(content.encode('UTF-8'))}
	proxy_url = "http://dayanjia.com/lily2t/"
	req = urllib2.Request(proxy_url, urllib.urlencode(postdata))
	response = urllib2.urlopen(req, timeout=20)