# coding: utf-8
from flask import *
import hashlib, random
import db, modules

def Run():
	if request.method == 'GET':
		return render_template('login.html')
	else:
		username, password = \
			request.form['username'], request.form['password']
		res = modules.ValidatePassword(username,password)
		if not res['success']:
			return modules.ReturnJSON(res)

		registered_username = db.Execute('SELECT username FROM users WHERE username=%s',username)[0]['username']
		client_key = hashlib.sha256((str(random.randint(1,10000000000))+username+password+"intoj").encode('utf-8')).hexdigest()
		if session.get('client_keys') == None:
			session['client_keys'] = {}
		session['client_keys'][client_key] = registered_username
		session.update()

		return modules.ReturnJSON({
			'success': True,
			'message': '登录成功！欢迎你，%s。' % registered_username,
			'username': registered_username,
			'client_key': client_key
		})
