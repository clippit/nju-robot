# -*- coding:utf-8 -*-

import codecs, re, sqlite3, urllib2
from datetime import datetime
from pyquery import PyQuery as pq
from multi_update import *


def generate_html(text):
	# Step 1: convert & < > to &amp; &lt; &gt;
	text = text.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
	# Step 2: make <p> and <br />
	text = text.replace('\r\n', '[-LB-]').replace('\n', '[-LB-]').replace('\r', '[-LB-]')
	text = text.replace(' ', '&nbsp;')
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
	text = re.sub(r'\[img\](.+?)\[\/img\]', 	# TODO: 图片是防盗链的，显示会有问题。。。。
	              r'<a href="\1" target="_blank"><img alt="" src="\1" /></a>', text)
	# Step 4: clear ANSI color code
	text = re.sub(r'\[[0-9;]{0,4}m', '', text)
	# Complete!
	return text

def store_data():
	"save backup to database"
	con = sqlite3.connect('./db.sqlite')
	cur = con.cursor()
	cur.execute( "INSERT INTO lilybbs_top10 (title, author, content, pub_time, link) VALUES(?, ?, ?, ?, ?)", (title, author, content, time, link) )
	cur.close()
	con.commit()
	con.close()

def update_blog():
	content_struct = { 'title': title,
	                   'description': content,
	                   'categories': [u'百合十大'],
	                   'custom_fields': [{'key': 'source', 'value': link},
	                                     {'key': 'author', 'value': author}]
	                 }
	blog.new_post(content_struct)

f = codecs.open('./lastupdate_bbstop10.log', 'r', 'utf-8')
last_update = f.readlines()
f.close()

log = open('./log.log', 'a')
top10_list = pq(url = 'http://bbs.nju.edu.cn/bbstop10') ('table a')

if len(top10_list) != 30:
	log.write( "%s - LilyBBS TOP10 fetch error!\n" % (datetime.now(),) )
	log.close()
	exit()

top10_list.make_links_absolute()
log.write( "%s - LilyBBS Top10 fetch successful!\n" % (datetime.now(),) )

f = open('./lastupdate_bbstop10.log', 'w')
for i in range(0,30,3):
	title = "[%s]%s" % ( pq(top10_list[i]).text(), pq(top10_list[i+1]).text(), )
	if title+'\n' not in last_update:
		#print title
		link = pq(top10_list[i+1]).attr.href # generate the thread link
		### handle Chinese cut off bug in LilyBBS system. Just fuck it!
		page = urllib2.urlopen(link).read()
		page = unicode(page, 'gbk', 'ignore') 
		if page[page.find(u'发信站')-1] != '\n':
			page = page.replace(u'发信站:', u'\n发信站:')
		### end
		page = pq(page) ('textarea').eq(0).text()
		header = re.match('.+\n.+\n.+\n', page).group() # header is the first 3 lines
		search_author = re.search(u'信人: (?P<id>[0-9A-Za-z]{2,12}) \(', header)
		author = search_author.group('id'); #generate the author's id
		search_datetime = re.search(u'南京大学小百合站 \((?P<time>[A-Za-z0-9: ]{24})', header)
		datetime_str = search_datetime.group('time').replace('  ', ' 0')
		time = datetime.strptime(datetime_str, '%a %b %d %H:%M:%S %Y') # generate the post time
		print '==========================\ntitle: %s\nauthor: %s\ntime: %s\n' % (title, author, time)
		content = generate_html( page[len(header)+1:] )

		log.write( "%s - source: %s\n%stitle:  %s\n" % ( datetime.now(), 'LilyBBS TOP10',' '*29, title.encode("utf-8"), ))
		
		store_data()
		update_blog()
	

	f.write(title.encode('UTF-8'))
	f.write('\n')
f.close()
log.close()