#!/usr/bin/python
# -*- coding:utf-8 -*-

import urllib2, oauth, urllib

#USERNAME = 'lily.studio.nju@gmail.com'
#PASSWORD = 'NJUl1ly'
APP_KEY = '1999053973'
APP_SECRET = 'd3de89c569f7cb593788e81606b6680d'
OAUTH_TOKEN = '1c61975dfe0e349ccf52cdfa8a6dbc07'
OAUTH_TOKEN_SECRET = 'af0940984164cfd97cf45b9729e7f0ba'
VERIFIER = '243585'
UPDATE_STATUS_URL = 'http://api.t.sina.com.cn/statuses/update.json'
CONSUMER_KEY = oauth.OAuthConsumer(APP_KEY, APP_SECRET)
TOKEN = oauth.OAuthToken(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
TOKEN.set_verifier(VERIFIER)

def get_request_header(url, method, param=None):
	oauth_request = oauth.OAuthRequest.from_consumer_and_token(CONSUMER_KEY, TOKEN, http_method=method, verifier=VERIFIER, http_url=url, parameters=param)
	oauth_request.sign_request(oauth.OAuthSignatureMethod_HMAC_SHA1(), CONSUMER_KEY, TOKEN)
	return oauth_request.to_header()

def unicode_urlencode(params):
	"""
	A unicode aware version of urllib.urlencode
	"""
	if isinstance(params, dict):
		params = params.items()
	return urllib.urlencode([(k, v.encode('utf-8')) for k, v in params])

def update(content):
	post_data = {'status': content}
	header = get_request_header(UPDATE_STATUS_URL, 'POST', post_data)
	req = urllib2.Request(UPDATE_STATUS_URL, unicode_urlencode(post_data), header)
	response = urllib2.urlopen(req)




# def update(content):
# 	base64string = base64.encodestring( '%s:%s' % (USERNAME, PASSWORD))[:-1]
# 	authheader = 'Basic %s' % base64string
# 	data = unicode_urlencode({'source':APPKEY, 'status': content})
# 	headers = {"Authorization": authheader}
# 	req = urllib2.Request('http://api.t.sina.com.cn/statuses/update.json', data, headers)
# 	response = urllib2.urlopen(req)
# 	return json.loads( response.read() )
