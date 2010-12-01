#!/usr/bin/python
# -*- coding:utf-8 -*-

import urllib2

def log(source,message):
	print ('%s ERROR: %s' % (source, message)).encode('UTF-8')
	if hasattr(log, 'write'):
		log.write( '%s - %s ERROR: %s' % (datetime.now(), source.encode('utf-8'), message.encode('utf-8'), ) )

#__all__ = ['blog','renren','sina','twitter','douban']

import pyblog, renren, sina

WORDPRESS_XMLRPC_URL = 'http://njulily.com/xmlrpc.php'
WORDPRESS_USERNAME = 'lilybot'
WORDPRESS_PASSWORD = 'imabot123'

# TEST ACCOUNT
WORDPRESS_XMLRPC_URL = 'http://localhost/xueshenghui/xmlrpc.php'
WORDPRESS_USERNAME = 'lilystudio'
WORDPRESS_PASSWORD = 'lilystudio'

def wordpress_new_post( title, content, categories=[], tags='', custom_fields=[] ):
	try:
		blog = pyblog.WordPress(WORDPRESS_XMLRPC_URL, WORDPRESS_USERNAME, WORDPRESS_PASSWORD)
		content_struct = { 'title': title,
		                   'description': content,
		                   'categories': categories,
		                   'mt_keywords': tags,
		                   'custom_fields': custom_fields}
		r = blog.new_post(content_struct)
	except pyblog.BlogError, e:
		log('wordpress', e.msg)
		return False
	return True


def renren_new_post(title, content):
	content = ''.join( (content, u'<p style="color:#800517;font-weight:bold;font-size:larger;">★★★更多精彩，敬请关注南京大学小百合工作室近期动态！</p>',) )
	try:
		s = renren.login()
		r = renren.add_blog(title, content, s['session_key'])
	except urllib2.URLError,e:
		log('renren',e.reason)
		return False
	return True if u'id' in r else False

def sina_new_microblog(content):
	try:
		r = sina.update(content)
	except urllib2.URLError,e:
		log('renren',e.reason)
		return False
	return True