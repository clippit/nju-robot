#!/usr/bin/python
# -*- coding:utf-8 -*-

import os, sys, codecs, re, sqlite3, urllib2, urllib, base64, traceback
from datetime import datetime
from pyquery import PyQuery as pq
import multi_update

path = os.path.abspath(os.path.dirname(sys.argv[0]))
GET_IMAGE = 'http://njulily.com/getimg.php?r='

def generate_html(text):
	# Step 1: convert & < > to &amp; &lt; &gt;
	text = text.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
	# Step 2: make <p> and <br />
	text = text.replace('\r\n', '[-LB-]').replace('\n', '[-LB-]').replace('\r', '[-LB-]')
	text = text.replace('[-LB-][-LB-]', '</p><p>').replace('[-LB-]', '<br />\n')
	text = ''.join( ('<p>', text, '</p>',) )
	text = text.replace('<p></p>','').replace('\r\n\r\n','').replace('</p><p>','</p>\n\n<p>')
	# Step 3: make font style
	text = re.sub(r'\[b\](.+?)\[\/b\]', r'<strong>\1</strong>', text)
	# Step 4: make <img> and <a>
	text = re.sub(r'(^|[^\"\'\]])(?i)(http|ftp|mms|rstp|news|https)\:\/\/([^\s\033\[\]\"\'\(\)<（）。，]+)',
	              r'\1[url]\2://\3[/url]', text)
	text = re.sub(r'\[url\]http\:\/\/(\S+\.)(?i)(gif|jpg|png|jpeg|jp)\[\/url\]',
	              r'[img]http://\1\2[/img]', text)
	text = re.sub(r'\[url\](.+?)\[\/url\]', r'<a href="\1" target="_blank">\1</a>', text)
	text = re.sub(r'\[img\](.+?)\[\/img\]',    # TODO: 图片是防盗链的，显示会有问题。。。。
	              r'<a href="\1" target="_blank"><img alt="" src="\1" /></a>', text)
	text = text.replace('  ', '&nbsp;&nbsp;')
	text = re.sub('\s+', ' ', text)              
	# Step 5 (MOVE TO read_post): clear ANSI color code
	#text = re.sub(r'\[[0-9;]*m', '', text)
	# Complete!
	return text
	
def read_url(url):
	'''handle Chinese cut off bug in LilyBBS system. Just fuck it!'''
	retries = 5
	while (retries>0):
		try:
			page = urllib2.urlopen(url, timeout=20).read().replace('\033','')
			page = unicode(page, 'gbk', 'ignore') 
			return page
		except Exception , what:
			print what
			retries -= 1
			print '######## Retrying.... ########'
	raise Exception("Read URL Failed!!!")

def read_post(page, n):
	raw = page.eq(n).text()
	if raw[raw.find(u'发信站')-1] != '\n':
		raw = raw.replace(u'发信站:', u'\n发信站:') # fix character cut off bug
	
	try:
		header = re.match('.+\n.+\n.+\n', raw).group() # header is the first 3 lines
	except:
		print 'Post Parsing Error!'
		log.write("%s - source: %s\n%s%s\n" % (datetime.now(), 'LilyBBS TOP10', ' '*29, 'POST PASRSING ERROR!!!', ))
		traceback.print_exc(file=sys.stdout)
		return
	
	raw = re.sub(r'\[[0-9;]*m', '', raw) # clear ANSI color code
	
	search_author = re.search(u'信人: (?P<id>[0-9A-Za-z]{2,12}) \(', header)
	author = ''.join( ('<a href="http://bbs.nju.edu.cn/bbsqry?userid=', search_author.group('id'), '" target="_blank">', search_author.group('id'), '</a>') ); #generate the author's id
	search_datetime = re.search(u'合站 \((?P<time>[A-Za-z0-9: ]{24})', header)
	datetime_str = search_datetime.group('time').replace('  ', ' 0')
	time = datetime.strptime(datetime_str, '%a %b %d %H:%M:%S %Y') # generate the post time
	tail_pos = raw.find(u'--\n\u203b \u6765\u6e90')
	content = generate_html( raw[len(header):tail_pos] )
	return (author, time, content,)

def store_data():
	"save backup to database"
	con = sqlite3.connect(path+'/db.sqlite')
	cur = con.cursor()
	cur.execute( "INSERT INTO lilybbs_top10 (title, author, content, pub_time, link) VALUES(?, ?, ?, ?, ?)", (title, author, content, time, link) )
	cur.close()
	con.commit()
	con.close()

def db_fetch(count=10):
	"get the latest several titles in database"
	con = sqlite3.connect(path+'/db.sqlite')
	cur = con.cursor()
	cur.execute( "SELECT id, title FROM lilybbs_top10 ORDER BY id DESC LIMIT ?", (count,) )
	result = cur.fetchall()
	cur.close()
	con.close()
	return [result[i][1] for i in range(count)]

def encode_url(match):
	url = urllib.pathname2url( base64.b64encode(match.group(1)) )
	return ''.join( ('<img alt="" src="', GET_IMAGE, url, '"') )

def image_proxy(text):
	return re.sub(r'<img alt="" src="([^"]+)"', encode_url, text)

def update_wordpress():
	categories = [u'百合十大']
	tags = '%s, %s' %('LilyBBS', board, )
	custom_fields = [{'key': 'source', 'value': friendly_link}, {'key': 'author', 'value': author}]
	if multi_update.wordpress_new_post(title, content, categories, tags, custom_fields, 0):
		print 'Wordpress Update Successful!'
		log.write( '%s - LilyBBS TOP10 - a new post to wordpress\n' % (datetime.now(),) )
	else:
		print 'Wordpress Update Failed!!!!'
		log.write( '%s - LilyBBS TOP10 - update wordpress failed!!!!!\n' % (datetime.now(),) )

def update_renren():
	renren_title = ''.join( (u'【百合十大】', title,) )
	renren_content = ''.join( (u'<p>原文地址：<a href="', friendly_link, '" target="_blank">', friendly_link, u'</a><br />原帖作者：', author, '</p>', image_proxy(content),) )
	renren_content = renren_content.replace('\r\n', '').replace('\n', '').replace('\r', '')
	if multi_update.renren_new_post(renren_title, renren_content):
		print 'Renren Update Successful!'
		log.write( '%s - LilyBBS TOP10 - a new post to renren\n' % (datetime.now(),) )
	else:
		print 'Renren Update Failed!!!!'
		log.write( '%s - LilyBBS TOP10 - update renren failed!!!!!\n' % (datetime.now(),) )

def update_sina():
	tweet = ''.join( (u'【#百合十大#】', title, ' ', friendly_link, ) )
	if multi_update.sina_new_microblog(tweet):
		print 'Sina Microblog Update Succesful!'
		log.write( '%s - LilyBBS TOP10 - a new microblog to sina\n' % (datetime.now(),) )
	else:
		print 'Sina Microblog Update Failed!!!'
		log.write( '%s - LilyBBS TOP10 - update sina microblog failed!!!!!\n' % (datetime.now(),) )

def update_douban():
	douban_title = ''.join( (u'【百合十大】', title,) )
	douban_text = pq(content).text()[:100]
	if multi_update.douban_new_recommendation(douban_title, douban_text, friendly_link):
		print 'Douban Update Succesful!'
		log.write( '%s - LilyBBS TOP10 - a new recommendation to douban\n' % (datetime.now(),) )
	else:
		print 'Douban Update Failed!!!'
		log.write( '%s - LilyBBS TOP10 - update douban recommendation failed!!!!!\n' % (datetime.now(),) )

def update_twitter():
	status = ''.join( (u'#百合十大 ', title, ' ', friendly_link, ) )
	if multi_update.twitter_new_status(status):
		print 'Twitter Update Succesful!'
		log.write( '%s - LilyBBS TOP10 - a new tweet to twitter\n' % (datetime.now(),) )
	else:
		print 'Twitter Update Failed!!!'
		log.write( '%s - LilyBBS TOP10 - update twitter failed!!!!!\n' % (datetime.now(),) )

f = codecs.open(path+'/lastupdate_bbstop10.log', 'r', 'utf-8')
last_update = f.readlines()
last_update = [last_update[i][:-1] for i in range( len(last_update) )]
f.close()

log = open(path+'/log.log', 'a')
try:
	top10_list = pq(url = 'http://bbs.nju.edu.cn/bbstop10', opener=read_url) ('table a')
except:
	log.write("%s - source: %s\n%s%s\n" % (datetime.now(), 'LilyBBS TOP10', ' '*29, 'FETCH TOP10 LIST FAILED!!!!!', ))
	traceback.print_exc(file=sys.stdout)
	print "subject get failed"
	exit()

if len(top10_list) != 30:
	log.write( "%s - LilyBBS TOP10 fetch error!\n" % (datetime.now(),) )
	log.close()
	exit()

top10_list.make_links_absolute()
log.write( "%s - LilyBBS Top10 fetch successful!\n" % (datetime.now(),) )

f = open(path+'/lastupdate_bbstop10.log', 'w')
for i in range(0,30,3):
	board = pq(top10_list[i]).text()
	title = "[%s]%s" % ( board, pq(top10_list[i+1]).text(), )
	if title not in last_update+db_fetch():
		print title.encode('UTF-8')
		link = pq(top10_list[i+1]).attr.href
		friendly_link = multi_update.short_url( ''.join( ('http://bbs.nju.edu.cn/main.html?', urllib.pathname2url(link[22:]), ) ) )# generate the thread link

		try:
			page = pq(url=link, opener=read_url) ('textarea')
		except:
			log.write("%s - source: %s\n%s%s\n" % (datetime.now(), 'LilyBBS TOP10', ' '*29, 'FETCH BBS POST FAILED!!!!!', ))
			traceback.print_exc(file=sys.stdout)
			continue
		
		original_post = read_post(page,0)
		author = original_post[0]
		time = original_post[1]
		sofa_post = read_post(page, 1)
		bench_post = read_post(page, 2)
		floor_post = read_post(page, 3)
		sofa = ''.join( (u'<li>沙发 ', sofa_post[0], u' 说：', sofa_post[2], '</li>', ) )
		bench = ''.join( (u'<li>板凳 ', bench_post[0], u' 说：', bench_post[2], '</li>', ) )
		floor = ''.join( (u'<li>地板 ', floor_post[0], u' 说：', floor_post[2], '</li>', ) )
		content = ''.join( (original_post[2], u'<h3>七嘴八舌</h3><ul class="responses">', sofa, bench, floor, '</ul>') )
		
		print ('==========================\ntitle: %s\nauthor: %s\ntime: %s\n' % (title, author, time) ).encode('UTF-8')
		log.write( "%s - source: %s\n%stitle:  %s\n" % ( datetime.now(), 'LilyBBS TOP10',' '*29, title.encode("utf-8"), ))
		
		try:
			store_data()
		except:
			log.write( "%s - source: %s\n%s%s\n" % ( datetime.now(), 'LilyBBS TOP10',' '*29, '!!!!! STORE DATA ERROR !!!!!', ))
			traceback.print_exc(file=sys.stdout)
		
		try:
			update_wordpress()
		except:
			log.write( "%s - source: %s\n%s%s\n" % ( datetime.now(), 'LilyBBS TOP10',' '*29, '!!!!! WORDPRESS UPDATE ERROR !!!!!', ))
			traceback.print_exc(file=sys.stdout)
		
		try:
			update_renren()
		except:
			log.write( "%s - source: %s\n%s%s\n" % ( datetime.now(), 'LilyBBS TOP10',' '*29, '!!!!! RENREN UPDATE ERROR !!!!!', ))
			traceback.print_exc(file=sys.stdout)
		
		try:
			update_douban()
		except:
			log.write( "%s - source: %s\n%s%s\n" % ( datetime.now(), 'LilyBBS TOP10',' '*29, '!!!!! DOUBAN UPDATE ERROR !!!!!', ))
			traceback.print_exc(file=sys.stdout)
		
		try:
			update_twitter()
		except:
			log.write( "%s - source: %s\n%s%s\n" % ( datetime.now(), 'LilyBBS TOP10',' '*29, '!!!!! TWITTER UPDATE ERROR !!!!!', ))
			traceback.print_exc(file=sys.stdout)
		
		try:
			update_sina()
		except:
			log.write( "%s - source: %s\n%s%s\n" % ( datetime.now(), 'LilyBBS TOP10',' '*29, '!!!!! SINA UPDATE ERROR !!!!!', ))
			traceback.print_exc(file=sys.stdout)

	

	f.write(title.encode('UTF-8'))
	f.write('\n')
f.close()
log.close()