#!/usr/bin/python
# -*- coding:utf-8 -*-

import os, sys, codecs, re, sqlite3, urllib2, json
from datetime import datetime
from pyquery import PyQuery as pq
import multi_update

path = os.path.abspath(os.path.dirname(sys.argv[0]))

################################################################################
###---###---### The following codes are the same with p_bbstop10 ###---###---###
def generate_html(text):
	# Step 1: convert & < > to &amp; &lt; &gt;
	text = text.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
	# Step 2: make <p> and <br />
	text = text.replace('\r\n', '[-LB-]').replace('\n', '[-LB-]').replace('\r', '[-LB-]')
	text = text.replace('  ', '&nbsp;&nbsp;')
	text = re.sub('\s+', ' ', text)
	text = text.replace('[-LB-][-LB-]', '</p><p>').replace('[-LB-]', '<br />\n')
	text = ''.join( ('<p>', text, '</p>',) )
	text = text.replace('<p></p>','').replace('\r\n\r\n','').replace('</p><p>','</p>\n\n<p>')
	# Step 3: make <img> and <a>
	text = re.sub(r'(^|[^\"\'\]])(?i)(http|ftp|mms|rstp|news|https)\:\/\/([^\s\033\[\]\"\'\(\)<（）。，]+)',
	              r'\1[url]\2://\3[/url]', text)
	text = re.sub(r'\[url\]http\:\/\/(\S+\.)(?i)(gif|jpg|png|jpeg|jp)\[\/url\]',
	              r'[img]http://\1\2[/img]', text)
	text = re.sub(r'\[url\](.+?)\[\/url\]', r'<a href="\1" target="_blank">\1</a>', text)
	text = re.sub(r'\[img\](.+?)\[\/img\]',    # TODO: 图片是防盗链的，显示会有问题。。。。
	              r'<a href="\1" target="_blank"><img alt="" src="\1" /></a>', text)
	# Step 4: clear ANSI color code
	text = re.sub(r'\[[0-9;]{0,4}m', '', text)
	# Complete!
	return text

def read_url(url):
	'''handle Chinese cut off bug in LilyBBS system. Just fuck it!'''
	page = urllib2.urlopen(url).read().replace('\033','')
	page = unicode(page, 'gbk', 'ignore') 
	return page
###---###---###   The above codes are the same with p_bbstop10   ###---###---###
################################################################################

def store_data():
	"save backup to database"
	con = sqlite3.connect(path+'/db.sqlite')
	cur = con.cursor()
	cur.execute( "INSERT INTO lilybbs_event (title, author, content, pub_time, link) VALUES(?, ?, ?, ?, ?)", (title, author, content, time, link) )
	cur.close()
	con.commit()
	con.close()

def update_wordpress():
	categories = [u'小百合BBS活动预告']
	tags = "%s, %s" % ('LilyBBS', board,)
	custom_fields = [{'key': 'source', 'value': friendly_link}, {'key': 'author', 'value': author}]
	if multi_update.wordpress_new_post(title, content, categories, tags, custom_fields):
		print 'Wordpress Update Successful!'
		log.write( '%s - LilyBBS Events - a new post to wordpress\n' % (datetime.now(),) )
	else:
		print 'Wordpress Update Failed!!!!'
		log.write( '%s - LilyBBS Events - update wordpress failed!!!!!\n' % (datetime.now(),) )

def update_renren():
	renren_title = ''.join( (u'【小百合BBS活动预告】', title,) )
	renren_content = ''.join( (u'<p>原文地址：<a href="', friendly_link, '" target="_blank">', friendly_link, u'</a><br />原帖作者：', author, '</p>', content,) )
	renren_content = renren_content.replace('\r\n', '').replace('\n', '').replace('\r', '')
	if multi_update.renren_new_post(renren_title, renren_content):
		print 'Renren Update Successful!'
		log.write( '%s - LilyBBS Events - a new post to renren\n' % (datetime.now(),) )
	else:
		print 'Renren Update Failed!!!!'
		log.write( '%s - LilyBBS Events - update renren failed!!!!!\n' % (datetime.now(),) )

def update_sina():
	content = ''.join( (u'【小百合BBS活动预告】', title, ' ', friendly_link, ) )
	if multi_update.sina_new_microblog(content):
		print 'Sina Microblog Update Succesful!'
		log.write( '%s - LilyBBS TOP10 - a new microblog to sina\n' % (datetime.now(),) )
	else:
		print 'Sina Microblog Update Failed!!!'
		log.write( '%s - LilyBBS TOP10 - update sina microblog failed!!!!!\n' % (datetime.now(),) )


f = codecs.open(path+'/lastupdate_bbsevent.log', 'r', 'utf-8')
last_update = f.readlines()
f.close()

log = open(path+'/log.log', 'a')
remote_resource = urllib2.urlopen('http://bbs.nju.edu.cn/cache/t_act.js')
event_str = unicode( remote_resource.read()[10:-25], 'gbk', 'ignore').replace("'",'"').replace('brd:','"brd":').replace('file:','"file":').replace('title:','"title":')
event_list = json.loads( event_str )

log.write( "%s - LilyBBS Events fetch successful!\n" % (datetime.now(),) )

f = open(path+'/lastupdate_bbsevent.log', 'w')
for i in range(0,len(event_list)):
	board = event_list[i]['brd']
	title = event_list[i]['title'] 
	if title+'\n' not in last_update:
		print title.encode('UTF-8')
		link = ''.join( ('http://bbs.nju.edu.cn/bbstcon?board=', event_list[i]['brd'], '&file=', event_list[i]['file']) )
		friendly_link = ''.join( ('http://bbs.nju.edu.cn/main.html?bbstcon%3Fboard%3D', event_list[i]['brd'], '%26file%3D', event_list[i]['file'], ) ) # generate the thread link
		################################################################################
		###---###---### The following codes are the same with p_bbstop10 ###---###---###
		### handle Chinese cut off bug in LilyBBS system. Just fuck it!
		#------UPDATE: move to read_url function------
		#page = urllib2.urlopen(link).read()
		#page = unicode(page, 'gbk', 'ignore') 
		#if page[page.find(u'发信站')-1] != '\n':
		#	page = page.replace(u'发信站:', u'\n发信站:')
		### end
		page = pq(url=link, opener=read_url) ('textarea').eq(0).text()
		if page[page.find(u'发信站')-1] != '\n':
			page = page.replace(u'发信站:', u'\n发信站:')
		header = re.match('.+\n.+\n.+\n', page).group() # header is the first 3 lines
		search_author = re.search(u'信人: (?P<id>[0-9A-Za-z]{2,12}) \(', header)
		author = ''.join( ('<a href="http://bbs.nju.edu.cn/bbsqry?userid=', search_author.group('id'), '" target="_blank">', search_author.group('id'), '</a>') ); #generate the author's id
		search_datetime = re.search(u'南京大学小百合站 \((?P<time>[A-Za-z0-9: ]{24})', header)
		datetime_str = search_datetime.group('time').replace('  ', ' 0')
		time = datetime.strptime(datetime_str, '%a %b %d %H:%M:%S %Y') # generate the post time
		print ('==========================\ntitle: %s\nauthor: %s\ntime: %s\n' % (title, author, time)).encode('UTF-8')
		content = generate_html( page[len(header)+1:] )
		###---###---###   The above codes are the same with p_bbstop10   ###---###---###
		################################################################################
		
		log.write( "%s - source: %s\n%stitle:  %s\n" % ( datetime.now(), 'LilyBBS Events',' '*29, title.encode("utf-8"), ))
		
		store_data()
		update_wordpress()
		update_renren()
		update_sina()
		
		
	f.write(title.encode('UTF-8'))
	f.write('\n')	
f.close()
log.close()