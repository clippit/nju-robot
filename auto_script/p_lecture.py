#!/usr/bin/python
# -*- coding:utf-8 -*-

import os, sys, codecs, re, sqlite3, urllib2, urllib, base64, traceback
from datetime import datetime
import multi_update

path = os.path.abspath(os.path.dirname(sys.argv[0]))

def postid2url(postid):
	return "http://njulily.com/post/%s" % (postid)

def update_wordpress(row):
	if row['type']==0:
		categories = [u'学术讲座']
	elif row['type']==1:
		categories = [u'校园活动']
	else:
		categories = []
	tags = '%s, %s, %s' % (row['keywords'], row['display_name'], row['speakers'],)
	custom_fields = [{'key': 'place',   'value': row['place']},
	                 {'key': 'time',    'value': row['coming_date'][4:16]},
	                 {'key': 'speaker', 'value': row['speakers']},
	                 {'key': 'host',    'value': row['display_name']}]
	post_id = multi_update.wordpress_new_post(row['post_title'], row['post_content'], categories, tags, custom_fields)
	if post_id:
		print 'Wordpress Update Successful!'
		log.write( '%s - Leture | Activity - a new post to wordpress\n' % (datetime.now(),) )
	else:
		print 'Wordpress Update Failed!!!!'
		log.write( '%s - Leture | Activity- update wordpress failed!!!!!\n' % (datetime.now(),) )
	return post_id

	
def update_renren(row,postid):
	if row['type']==0:
		title=u'【学术讲座预告】%s' % (row['post_title'])
		content = u'<p>时间：%s<br />地点：%s<br />主讲人：%s<br />链接：<a href="%s" alt="" target="_blank">%s</a></p>%s' % (row['coming_date'][:16], row['place'], row['speakers'], postid2url(postid), postid2url(postid), row['post_content'],)
	elif row['type']==1:
		title=u'【校园活动预告】%s' % (row['post_title'])
		content = u'<p>时间：%s<br />地点：%s<br />主办：%s<br />链接：<a href="%s" alt="" target="_blank">%s</a></p>%s' % (row['coming_date'][:16], row['place'], row['display_name'], postid2url(postid), postid2url(postid), row['post_content'],)
	else:
		title =u'【预告】%s' % (row['post_title'])
		content = u'<p>时间：%s<br />地点：%s<br />链接：<a href="%s" alt="" target="_blank">%s</a></p>%s' % (row['coming_date'][:16], row['place'], postid2url(postid), postid2url(postid), row['post_content'],)
	if multi_update.renren_new_post(title, content):
		print 'Renren Update Successful!'
		log.write( '%s - Leture | Activity - a new post to renren\n' % (datetime.now(),) )
	else:
		print 'Renren Update Failed!!!!'
		log.write( '%s - Leture | Activity - update renren failed!!!!!\n' % (datetime.now(),) )
	

def update_douban(row,postid):
	if row['type']==0:
		title =u'【学术讲座预告】%s' % (row['post_title'])
		excerpt = u'时间：%s 地点：%s 主讲人：%s  --  %s' % (row['coming_date'][4:16], row['place'], row['speakers'], row['post_content'][:50], )
	elif row['type']==1:
		title =u'【校园活动预告】%s' % (row['post_title'])
		excerpt = u'时间：%s 地点：%s 主办：%s  --  %s' % (row['coming_date'][4:16], row['place'], row['display_name'], row['post_content'][:50], )
	else:
		title =u'【预告】%s' % (row['post_title'])
		excerpt = u'时间：%s 地点：%s  --  %s' % (row['coming_date'][4:16], row['place'], row['post_content'][:50], )
	if multi_update.douban_new_recommendation(title, excerpt, postid2url(postid)):
		print 'Douban Update Succesful!'
		log.write( '%s - Leture | Activity - a new recommendation to douban\n' % (datetime.now(),) )
	else:
		print 'Douban Update Failed!!!'
		log.write( '%s - Leture | Activity - update douban recommendation failed!!!!!\n' % (datetime.now(),) )

def make_status(row,postid):
	if row['type']==0:
		status =u'【学术讲座预告】%s 时间：%s 地点：%s %s' % (row['post_title'][:70], row['coming_date'][4:16], row['place'], postid2url(postid))
	elif row['type']==1:
		status =u'【校园活动预告】%s 时间：%s 地点：%s %s' % (row['post_title'][:70], row['coming_date'][4:16], row['place'], postid2url(postid))
	else:
		status =u'【预告】%s 时间：%s 地点：%s %s' % (row['post_title'][:70], row['coming_date'][4:16], row['place'], postid2url(postid))
	return status

def update_sina(row,postid):
	if multi_update.sina_new_microblog(make_status(row,postid)):
		print 'Sina Microblog Update Succesful!'
		log.write( '%s - Leture | Activity - a new microblog to sina\n' % (datetime.now(),) )
	else:
		print 'Sina Microblog Update Failed!!!'
		log.write( '%s - Leture | Activity - update sina microblog failed!!!!!\n' % (datetime.now(),) )

def update_twitter(row,postid):
	if multi_update.twitter_new_status(make_status(row,postid)):
		print 'Twitter Update Succesful!'
		log.write( '%s - LilyBBS TOP10 - a new tweet to twitter\n' % (datetime.now(),) )
	else:
		print 'Twitter Update Failed!!!'
		log.write( '%s - LilyBBS TOP10 - update twitter failed!!!!!\n' % (datetime.now(),) )



log = open(path+'/log.log', 'a')

con = sqlite3.connect(path+'/db.sqlite')
con.row_factory = sqlite3.Row
cur = con.cursor()
cur.execute("SELECT * FROM posts p join users u on p.uid = u.uid WHERE p.statue=1 AND (julianday(p.coming_date)-julianday(datetime(CURRENT_TIMESTAMP,'localtime')))<4;")

for row in cur:
	print row['post_title'].encode("utf-8")
	log.write( "%s - source: %s\n%stitle:  %s\n" % ( datetime.now(), 'Lecture | Activity',' '*29, row['post_title'].encode("utf-8"), ) )
	try:
		postid = update_wordpress(row)
		update_renren(row, postid)
		update_douban(row, postid)
		update_twitter(row, postid)
		update_sina(row, postid)
		updatecur = con.cursor()
		updatecur.execute("UPDATE posts SET status = 0 WHERE pid = ?", (row['pid']))
		updatecur.commit()
		updatecur.close()
	except:
		log.write( "%s - source: %s\n%s%s\n" % ( datetime.now(), 'Lecture | Activity',' '*29, '!!!!! UPDATE DATA ERROR !!!!!', ))
		traceback.print_exc(file=sys.stdout)
log.close()
cur.close()
con.close()
	