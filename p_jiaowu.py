#!/usr/bin/python
# -*- coding:utf-8 -*-

import os, sys, codecs, re, sqlite3
from datetime import datetime
from pyquery import PyQuery as pq
import multi_update

path = os.path.abspath(os.path.dirname(sys.argv[0]))

def html_cleanup(html):
	"clean up the markup of jiaowu news"
	html = html.replace('&#13;','\n')
	html = re.sub(r'\s(style|lang|class|id|dir|size)="[^"]*"', '', html) #remove style, lang, class, dir properties in markup
	html = re.sub(r'<\/?(span|font)\s?\/?>', '', html) #remove all <span>
	html = re.sub(r'<(\w+)>[\s|(\xc2\xa0)]*<\/\1>', '', html) #remove all blank tags
	return html
	
def store_data():
	"save backup to database"
	con = sqlite3.connect(path+'/db.sqlite')
	cur = con.cursor()
	cur.execute( "INSERT INTO jiaowu (title, date, content, link) VALUES(?, ?, ?, ?)", (title, date, content, link) )
	cur.close()
	con.commit()
	con.close()

def update_wordpress():
	if u'国际交流' in title:
		categories = [u'国际交流']
	else:
		categories = [u'教务通知']
	custom_fields = [{'key': 'source', 'value': link}]
	if multi_update.wordpress_new_post(title, content, categories,'' , custom_fields):
		print 'Wordpress Update Successful!'
		log.write( '%s - Jiaowu News - a new post to wordpress\n' % (datetime.now(),) )
	else:
		print 'Wordpress Update Failed!!!!'
		log.write( '%s - Jiaowu News - update wordpress failed!!!!!\n' % (datetime.now(),) )

def update_renren():
	renren_title = ''.join( (u'【教务处通知】', title,) )
	renren_content = ''.join( (content, u'<p>原文地址：<a href="', link, '" target="_blank">', link, '</a></p>',) )
	renren_content = renren_content.replace('\r\n', '').replace('\n', '').replace('\r', '')
	if multi_update.renren_new_post(renren_title, renren_content):
		print 'Renren Update Successful!'
		log.write( '%s - Jiaowu News - a new post to renren\n' % (datetime.now(),) )
	else:
		print 'Renren Update Failed!!!!'
		log.write( '%s - Jiaowu News - update renren failed!!!!!\n' % (datetime.now(),) )


f = codecs.open(path+'/lastupdate_jiaowu.log', 'r', 'utf-8')
last_update = f.readlines()
f.close()

log = open(path+'/log.log', 'a')
news_list = pq(url='http://jw.nju.edu.cn/root/index.html') ('td#demo1 table table a')
news_list.make_links_absolute()
log.write( "%s - jiaowu fetch successful!\n" % (datetime.now(),) )

f = open(path+'/lastupdate_jiaowu.log', 'w')
for i in range(9, -1, -1):
	news = pq(news_list[i])
	title = news.attr.title # generate the title
	if title+'\n' not in last_update: # start updating
		print title.encode('UTF-8')
		print '============================='
		link = news.attr.href
		d = pq(url = link)
		print 'debug----link: %s' % (link)
		d.make_links_absolute()
		date_str = d('div#d table tr').eq(1).find('table td').eq(1).text()[1:-1]
		date = datetime.strptime(date_str, "%Y-%m-%d") # generate public date
		print 'debug----date: %s' % (date)
		content = html_cleanup( d('div#d form td').eq(0).html() ) # generate main content
		attachment = d('div#d form tr').eq(1).find('a')
		if attachment.text() is not None: # generate attachments list
			content = u''.join((content, u'<h3>相关文件</h3><ul>',))
			for e in attachment:
				a = pq(e)
				content = u''.join((content, '<li><a href="', a.attr.href, '">', a.text(), '</a></li>', ))
			content = u''.join((content, u'</ul>',))
		#print "debug----content:\n%s" % (content)
		
		log.write( "%s - source: %s\n%stitle:  %s\n" % ( datetime.now(), 'jiaowu',' '*29, title.encode("utf-8"), ))
		
		store_data()
		#log.write("%s%s\n" % ( ' '*29, 'save to database successful' ))
		update_wordpress()
		update_renren()
		
	f.write(news.attr.title.encode("utf-8"))
	f.write('\n')
f.close()
log.close()
