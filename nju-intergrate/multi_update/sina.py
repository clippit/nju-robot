#!/usr/bin/python
# -*- coding:utf-8 -*-

import urllib, urllib2, base64, json

USERNAME = 'lily.studio.nju@gmail.com'
PASSWORD = 'NJUl1ly'
APPKEY = '1999053973'

def unicode_urlencode(params):
	"""
	A unicode aware version of urllib.urlencode
	"""
	if isinstance(params, dict):
		params = params.items()
	return urllib.urlencode([(k, v.encode('utf-8')) for k, v in params])


def update(content):
	base64string = base64.encodestring( '%s:%s' % (USERNAME, PASSWORD))[:-1]
	authheader = 'Basic %s' % base64string
	data = unicode_urlencode({'source':APPKEY, 'status': content})
	headers = {"Authorization": authheader}
	req = urllib2.Request('http://api.t.sina.com.cn/statuses/update.json', data, headers)
	response = urllib2.urlopen(req)
	return json.loads( response.read() )
