#coding:utf-8
from flask import *
import json, hashlib
import db, config

def ReturnJSON(data):
	return Response(json.dumps(data),mimetype='application/json')
def RedirectBack( error_message = None , ok_message = None ):
	if error_message != None:
		flash(error_message,'error')
	if ok_message != None:
		flash(ok_message,'ok')
	url = request.referrer
	if url == None: url = '/'
	return redirect(url)

def ParseInt( s , default = 0 , limit_l = int(-1e9) ,limit_r = int(1e9) ):
	if s == None or not s.isdigit(): return default
	s = int(s)
	if s < limit_l or s > limit_r: return default
	return s
def GetCurrentPage():
	return ParseInt(request.args.get('page'),1,1,1e9)

def IsVaildUsername(username):
	if len(username) == 0 or len(username) > 15:
		return False
	banned_chars = ['\n','\r','\b','\t','<','>','/','\\','\'','"','&','#','?','%','$','#','@','!','(',')','[',']','{','}']
	for char in banned_chars:
		if username.count(char) != 0:
			return False
	return True
def ValidatePassword(username,password):
	if username == None or password == None:
		return { 'success': False, 'message': '缺少用户名或密码' }
	std_password_list = db.Execute('SELECT password,salt FROM users WHERE username=%s',username)
	if len(std_password_list) == 0:
		return { 'success': False, 'message': '无此用户' }
	std_password, salt = \
		std_password_list[0]['password'], std_password_list[0]['salt']
	if std_password != hashlib.sha256(('intoj'+password+salt).encode('utf-8')).hexdigest():
		return { 'success': False, 'message': '密码错误' }
	return { 'success': True, 'message': 'ok' }
def ValidateClientkey(username,client_key):
	if username == None or client_key == None or session.get('client_keys') == None:
		return False
	return session['client_keys'].get(client_key) == username
def GetCurrentOperator():
	if not ValidateClientkey(request.cookies.get('username'),request.cookies.get('client_key')):
		return None
	return request.cookies.get('username')

def GetGravatarEmailHash(username,email):
	if email == None or len(email.strip()) == 0:
		email = username + "intoj2333"
	return hashlib.md5(email.strip().lower().encode('utf-8')).hexdigest()
def GetGravatarAddress(username,email,size=64):
	hash = GetGravatarEmailHash(username,email)
	return config.config['site']['gravatar_prefix'] + hash + "?s=%d&d=identicon"%size