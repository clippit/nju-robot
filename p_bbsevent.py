# -*- coding:utf-8 -*-

import codecs, re, sqlite3, urllib2, json
from datetime import datetime
from pyquery import PyQuery as pq
import multi_update
from p_bbstop10 import generate_html

def store_data():
	"save backup to database"
	con = sqlite3.connect('./db.sqlite')
	cur = con.cursor()
	cur.execute( "INSERT INTO lilybbs_event (title, author, content, pub_time, link) VALUES(?, ?, ?, ?, ?)", (title, author, content, time, link) )
	cur.close()
	con.commit()
	con.close()

def update_wordpress():
	categories = [u'小百合BBS活动预告']
	custom_fields = [{'key': 'source', 'value': link}, {'key': 'author', 'value': author}]
	if multi_update.wordpress_new_post(title, content, categories, custom_fields):
		print 'Wordpress Update Successful!'
		log.write( '%s - LilyBBS Events - a new post to wordpress\n' % (datetime.now(),) )
	else:
		print 'Wordpress Update Failed!!!!'
		log.write( '%s - LilyBBS Events - update wordpress failed!!!!!\n' % (datetime.now(),) )

def update_renren():
	renren_title = ''.join( (u'【小百合BBS活动预告】', title,) )
	renren_content = ''.join( (u'<p>原文地址：<a href="', link, '" target="_blank">', link, u'</a><br />原帖作者：', author, '</p>', content,) )
	renren_content = renren_content.replace('\r\n', '').replace('\n', '').replace('\r', '')
	if multi_update.renren_new_post(renren_title, renren_content):
		print 'Renren Update Successful!'
		log.write( '%s - LilyBBS Events - a new post to renren\n' % (datetime.now(),) )
	else:
		print 'Renren Update Failed!!!!'
		log.write( '%s - LilyBBS Events - update renren failed!!!!!\n' % (datetime.now(),) )



f = codecs.open('./lastupdate_bbstop10.log', 'r', 'utf-8')
last_update = f.readlines()
f.close()

log = open('./log.log', 'a')
remote_resource = urllib2.urlopen('http://bbs.nju.edu.cn/cache/t_act.js')
event_str = unicode( remote_resource.read()[10:-25], 'gbk', 'ignore').replace("'",'"').replace('brd:','"brd":').replace('file:','"file":').replace('title:','"title":')
event_list = json.loads( event_str )

log.write( "%s - LilyBBS Events fetch successful!\n" % (datetime.now(),) )

f = open('./lastupdate_bbsevent.log', 'w')
for i in range(0,len(event_list)):
	title = event_list[i]['title'] 
	if title+'\n' not in last_update:
		print title
		link = ''.join( ('http://bbs.nju.edu.cn/bbstcon?board=', event_list[i]['brd'], '&file=', event_list[i]['file']) ) # generate the thread link
		
		################################################################################
		###---###---### The following codes are the same with p_bbstop10 ###---###---###
		### handle Chinese cut off bug in LilyBBS system. Just fuck it!
		page = urllib2.urlopen(link).read()
		page = unicode(page, 'gbk', 'ignore') 
		if page[page.find(u'发信站')-1] != '\n':
			page = page.replace(u'发信站:', u'\n发信站:')
		### end
		page = pq(page) ('textarea').eq(0).text()
		header = re.match('.+\n.+\n.+\n', page).group() # header is the first 3 lines
		search_author = re.search(u'信人: (?P<id>[0-9A-Za-z]{2,12}) \(', header)
		author = ''.join( ('<a href="http://bbs.nju.edu.cn/bbsqry?userid=', search_author.group('id'), '" target="_blank">', search_author.group('id'), '</a>') ); #generate the author's id
		search_datetime = re.search(u'南京大学小百合站 \((?P<time>[A-Za-z0-9: ]{24})', header)
		datetime_str = search_datetime.group('time').replace('  ', ' 0')
		time = datetime.strptime(datetime_str, '%a %b %d %H:%M:%S %Y') # generate the post time
		print '==========================\ntitle: %s\nauthor: %s\ntime: %s\n' % (title, author, time)
		content = generate_html( page[len(header)+1:] )
		###---###---###   The above codes are the same with p_bbstop10   ###---###---###
		################################################################################
		
		log.write( "%s - source: %s\n%stitle:  %s\n" % ( datetime.now(), 'LilyBBS Events',' '*29, title.encode("utf-8"), ))
		
		store_data()
		update_wordpress()
		update_renren()
		
		
	f.write(title.encode('UTF-8'))
	f.write('\n')	
f.close()
log.close()