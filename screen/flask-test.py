# -*- coding: utf-8 -*-
# author: bing
# 

import pymysql, time
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

@app.route('/<name>')
def index(name=None):
	db = pymysql.connect(host = "127.0.0.1", port = 3306, user = "root", passwd = "test@11~", db = "tt",charset="utf8")
	cursor = db.cursor()
	sql = 'select * from user where name = {0}'.format(name)
	cursor.execute(sql)
	row = cursor.fetchall()
	return row.__str__()

@app.route('/test', methods=['GET', 'POST'])
def test():
	if request.method == "POST":
		tt = request.values.get("name", 0)
		print(tt)
		db = pymysql.connect(host = "127.0.0.1", port = 3306, user = "root", passwd = "test@11~", db = "tt",charset="utf8")
		cursor = db.cursor()
		sql = 'select * from user where name = "{0}"'.format(tt)
		cursor.execute(sql)
		row = cursor.fetchall()
		return row.__str__()
	else:
		return request.args.get('key', '')


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)

