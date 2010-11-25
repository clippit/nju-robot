#!/usr/bin/python

__all__ = ['blog','renren','sina','twitter','douban']

import pyblog

WORDPRESS_XMLRPC_URL = 'http://localhost/xueshenghui/xmlrpc.php'
WORDPRESS_USERNAME = 'lilystudio'
WORDPRESS_PASSWORD = 'lilystudio'

blog = pyblog.WordPress(WORDPRESS_XMLRPC_URL, WORDPRESS_USERNAME, WORDPRESS_PASSWORD)

RENREN_USERNAME = ''
RENREN_PASSWORD = ''

