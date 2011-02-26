#!/usr/bin/python
# -*- coding:utf-8 -*-

import urllib2, urllib, hashlib, json
from datetime import datetime

LOGIN_URL = 'http://login.api.renren.com/CL.do'
API_URL = 'http://m1.api.renren.com/restserver.do'
API_KEY = 'db1ffe772f504e9790907be9c9a651c7'
SECRET_KEY = 'a13bb175bc1940f6b78807e58329264f'

RENREN_USERNAME = 'njulilystudio@126.com'
RENREN_PASSWORD = '2d41d2433df7f8090af29a76c1d4822c'

# TEST ACCOUNT
#RENREN_USERNAME = 'wxing123'
#RENREN_PASSWORD = '71c1ebc28e10a4acea02f8ffb28ee54f'


def unicode_urlencode(params):
	"""
	A unicode aware version of urllib.urlencode
	"""
	if isinstance(params, dict):
		params = params.items()
	return urllib.urlencode([(k, v.encode('utf-8')) for k, v in params])

def make_sig(args):
	"""
	Return md5 signature of Renren post data
	"""
	m = hashlib.md5()
	#m.update( ''.join( [u'%s=%s' % (unicode_encode(x), unicode_encode(args[x])) for x in sorted(args.keys())] ).encode('utf-8') )
	m.update( ''.join( ['%s=%s' % (x.encode('utf-8'), args[x].encode('utf-8')) for x in sorted(args.keys())] ) )
	m.update(SECRET_KEY)
	return m.hexdigest()

def send_request(url, params):
	params['sig'] = make_sig(params)
	headers = {'User-agent': ''}
	req = urllib2.Request(url, unicode_urlencode(params), headers)
	response = urllib2.urlopen(req)
	return json.load ( response )

def login():
	login_request = {'check' : '0', 
	                 'user' : RENREN_USERNAME, 
	                 'clientName' : 'renren', 
	                 'model' : 'gen', 
	                 'version' : '20100317', 
	                 'login_info' : '{"ver":"2.2.0.20100317","cellid":"0","from":9100201}', 
	                 'format' : 'json', 
	                 'password' : RENREN_PASSWORD, 
	                 'v' : '1.0', 
	                 'api_key' : API_KEY, 
	                 'session_key' : '' }
	return send_request(LOGIN_URL, login_request)

def add_blog(title, content, session_key):
	add_blog_request = {'v' : '1.1', 
	                    'content' : content, 
	                    'session_key' : session_key, 
	                    'api_key' : API_KEY, 
	                    'format' : 'json', 
	                    'title' : title, 
	                    'cate_id' : '0', 
	                    'method' : 'phoneclient.addBlog' }
	return send_request(API_URL, add_blog_request)


