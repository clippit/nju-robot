#!/usr/bin/python
# -*- coding:utf-8 -*-

con = sqlite3.connect(path+'/db.sqlite')
cur = con.cursor()
cur.execute("SELECT * from posts WHERE statue=0")
result = cur.fetchall()
cur.close()
