#coding:utf-8
from flask import *
import db, modules, config
import hashlib

def GetUserInfo(username):
	res = db.Execute('SELECT * FROM users WHERE username=%s',username)
	if len(res) == 0: return None
	res = res[0]
	return {
		'username': res['username'],
		'email': res['email'],
		'sex': res['sex'],
		'motto': res['motto'],
		'realname': res['realname'],
		'background-url': res['background-url'],
		'rating': res['rating']
	}

def UserListRun():
	per_page = config.config['site']['per_page']['user_ranklist']
	current_page = modules.GetCurrentPage()
	users = db.Execute('SELECT * FROM users ORDER BY rating DESC LIMIT %s OFFSET %s',(per_page,per_page*(current_page-1)))
	return render_template('userlist.html',users=users,current_page=current_page)

def UserHomeRun(username):
	userinfo = GetUserInfo(username)
	if userinfo == None:
		return modules.RedirectBack('无此用户')
	return render_template('userhome.html',user=userinfo)

def UserEditRun(username):
	userinfo = GetUserInfo(username)
	username = userinfo['username']
	if userinfo == None:
		return modules.RedirectBack('无此用户')
	operator = modules.GetCurrentOperator()
	if operator == None:
		return modules.RedirectBack('请先登录')
	if operator != username:
		return modules.RedirectBack('无此权限')

	if request.method == 'GET':
		return render_template('useredit.html',user=userinfo)
	else:
		if not modules.ValidatePassword(request.cookies.get('username'),request.form['password'])['success']:
			return modules.RedirectBack('密码错误（密码应是当前登录的用户的密码）')
		if len(request.form['new_password'].strip()) != 0:
			new_password = request.form['new_password'].strip()
			if new_password != request.form['repeat_new_password'].strip():
				return modules.RedirectBack('「新密码」与「确认新密码」不符')
			salt = db.Execute('SELECT salt FROM users WHERE username=%s',username)[0]['salt']
			new_password_hash = hashlib.sha256(("intoj"+new_password+salt).encode('utf-8')).hexdigest()
			db.Execute('UPDATE users SET password=%s WHERE username=%s',(new_password_hash,username))

		db.Execute('UPDATE users SET `email`=%s,`realname`=%s,`motto`=%s,`background-url`=%s WHERE username=%s',
			(request.form['email'],request.form['realname'],request.form['motto'],request.form['background-url'],username))
		return modules.RedirectBack( ok_message = '修改成功' )
