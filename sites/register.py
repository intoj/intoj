# coding: utf-8
from flask import *
import hashlib
import config, db, modules

def Run():
	if request.method == 'GET':
		if not config.config['security']['allow_registration']:
			flash('先提醒一句：当前禁止注册。如需要注册，请联系管理员。','error')
		return render_template('register.html')
	else:
		if not config.config['security']['allow_registration']:
			return modules.ReturnJSON({ 'success': False, 'message': '当前禁止注册' })
		username, password, repeat_password, salt = \
			request.form['username'], request.form['password'], request.form['repeat_password'], request.form['salt']
		if password != repeat_password:
			return modules.ReturnJSON({ 'success': False, 'message': '两次输入的密码不同' })
		if len(username) == 0:
			return modules.ReturnJSON({ 'success': False, 'message': '你注册一个空用户名干啥' })
		if not modules.IsVaildUsername(username):
			return modules.ReturnJSON({ 'success': False, 'message': '非法的用户名' })
		same_username_cnt = db.Execute('SELECT COUNT(*) FROM users WHERE username=%s',username)[0]['COUNT(*)']
		if same_username_cnt != 0:
			return modules.ReturnJSON({ 'success': False, 'message': '该用户名已被注册' })
		if password == hashlib.sha256(('intoj'+salt).encode('utf-8')).hexdigest():
			return modules.ReturnJSON({ 'success': False, 'message': '你的密码好短啊' })
		db.Execute('INSERT INTO users VALUES(NULL,%s,%s,%s,"",0,"","","",1500)',(username,password,salt))
		return modules.ReturnJSON({ 'success': True, 'message': '注册成功！欢迎你，%s。<br />前去登录吧！'%username })
