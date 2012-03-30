#!/usr/bin/python
# -*- coding:utf-8 -*-

import urllib2
import config

def log(source, message):
	print ('%s ERROR: %s' % (source, message)).encode('UTF-8')
	if hasattr(log, 'write'):
		log.write( '%s - %s ERROR: %s' % (datetime.now(), source.encode('utf-8'), message.encode('utf-8'), ) )


def short_url(url):
	re = urllib2.urlopen('%s%s' % (config.URL_SHORTER_API, url,))
	return re.read()


#__all__ = ['blog','renren','sina','twitter','douban']

import pyblog, renren, sina, douban, twitter


def wordpress_new_post( title, content, categories=[], tags='', custom_fields=[], allow_comment=1 ):
	try:
		blog = pyblog.WordPress(config.WORDPRESS_XMLRPC_URL, config.WORDPRESS_USERNAME, config.WORDPRESS_PASSWORD)
		content_struct = { 'title': title,
		                   'description': content,
		                   'categories': categories,
		                   'mt_keywords': tags,
		                   'custom_fields': custom_fields,
		                   'mt_allow_comments': allow_comment}
		r = blog.new_post(content_struct)
	except pyblog.BlogError, e:
		log('wordpress', e.msg)
		return False
	return r


def renren_new_post(title, content):
	#content = ''.join( (content, u'<p style="color:#800517;font-weight:bold;font-size:larger;">★★★百合有聊 <a href="http://blog.njulily.com">http://blog.njulily.com</a>，更多新鲜，更多色彩！</p>',) )
	try:
		s = renren.login()
		r = renren.add_blog(title, content, s['session_key'])
	#	s2 = renren.login_another()
	#	r2 = renren.add_blog(title, content, s2['session_key'])
	except urllib2.HTTPError,e:
		log('renren',e.code)
		return False
	except urllib2.URLError,e:
		log('renren',e.reason)
		return False
	return True if u'id' in r else False

def sina_new_microblog(content):
	try:
		r = sina.update(content)
	except urllib2.HTTPError,e:
		log('sina',e.code)
		return False
	except urllib2.URLError,e:
		log('sina',e.reason)
		return False

	return True

def douban_new_recommendation(title, excerpt, link):
	try:
		douban.add_recommendation(title, excerpt, link)
	except urllib2.HTTPError,e:
		log('douban',e.code)
		return False
	except urllib2.URLError,e:
		log('douban',e.reason)
		return False
	return True

def twitter_new_status(content):
	try:
		twitter.status_update(content)
	except urllib2.HTTPError,e:
		log('twitter',e.code)
		return False
	except urllib2.URLError,e:
		log('twitter',e.reason)
		return False
	return True
