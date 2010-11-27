#!/usr/bin/python

import urllib2

def log(source,message):
	print '%s ERROR: %s' % (source, message)
	if hasattr(log, 'write'):
		log.write( '%s - %s ERROR: %s' % (datetime.now(), source.encode('utf-8'), message.encode('utf-8'), ) )

#__all__ = ['blog','renren','sina','twitter','douban']

import pyblog, renren

WORDPRESS_XMLRPC_URL = 'http://localhost/xueshenghui/xmlrpc.php'
WORDPRESS_USERNAME = 'lilystudio'
WORDPRESS_PASSWORD = 'lilystudio'

def wordpress_new_post( title, content, categories=[], custom_fields=[] ):
	try:
		blog = pyblog.WordPress(WORDPRESS_XMLRPC_URL, WORDPRESS_USERNAME, WORDPRESS_PASSWORD)
		content_struct = { 'title': title,
		                   'description': content,
		                   'categories': categories,
		                   'custom_fields': custom_fields}
		r = blog.new_post(content_struct)
	except pyblog.BlogError, e:
		log('wordpress', e.msg)
		return False
	return True


def renren_new_post(title, content):
	try:
		s = renren.login()
		r = renren.add_blog(title, content, s['session_key'])
	except urllib2.URLError,e:
		log('renren',e.reason)
		return False
	return True if u'id' in r else False

