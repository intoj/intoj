# coding: utf-8
from flask import *
import hashlib
import config, db, modules

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
	total_page = (db.Execute('SELECT COUNT(*) FROM users')[0]['COUNT(*)']+per_page-1) / per_page;
	users = db.Execute('SELECT * FROM users ORDER BY rating DESC LIMIT %s OFFSET %s',(per_page,per_page*(current_page-1)))
	return render_template('userlist.html',users=users,pageinfo={ 'per': per_page, 'tot': total_page })

def UserHomeRun(username):
	userinfo = GetUserInfo(username)
	if userinfo == None:
		return modules.RedirectBack('无此用户')
	return render_template('userhome.html',user=userinfo)

def UserEditRun(username):
	userinfo = GetUserInfo(username)
	if userinfo == None:
		return modules.RedirectBack('无此用户')
	username = userinfo['username']

	operator = modules.GetCurrentOperator()
	if operator == None:
		return modules.RedirectBack('请先登录')
	if operator != username and not modules.CheckPrivilege(operator,'user_manager'):
		return modules.RedirectBack('无此权限')

	if request.method == 'GET':
		return render_template('useredit.html',user=userinfo)
	else:
		if not modules.ValidatePassword(operator,request.form['password'])['success']:
			return modules.RedirectBack('密码错误（密码应是当前登录的用户的密码）')
		if len(request.form['realname']) > 16:
			return modules.RedirectBack('真实姓名过长（限制为 16 字符）')
		if not modules.IsVaildUsername(request.form['realname']):
			return modules.RedirectBack('真实姓名中不能包含特殊符号')
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
