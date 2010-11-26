#!/usr/bin/python

__all__ = ['blog','renren','sina','twitter','douban']

import pyblog

WORDPRESS_XMLRPC_URL = 'http://localhost/xueshenghui/xmlrpc.php'
WORDPRESS_USERNAME = 'lilystudio'
WORDPRESS_PASSWORD = 'lilystudio'

blog = pyblog.WordPress(WORDPRESS_XMLRPC_URL, WORDPRESS_USERNAME, WORDPRESS_PASSWORD)

RENREN_USERNAME = 'zlthooray@gmail.com'
RENREN_PASSWORD = '4c88e832b83178ed608ce7cba0d5a71a'

