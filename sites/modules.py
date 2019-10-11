#coding:utf-8
from flask import *
import json, hashlib
import db, config

def IsSafeFilePath(filepath):
	return '..' not in filepath

def GetColorOfScore(a,fullscore=100):
	a = float(a)
	fullscore = float(fullscore)
	if a <= fullscore/2:
		g = int( (a/fullscore) * (255+255-80) )
		return "rgb(255,%d,0)" % g
	else:
		r = int( (1.0-a/fullscore) * (255+255) )
		return "rgb(%d,220,0)" % r

def IsEmpty(s):
	return s == None or s.strip() == ''
def ScoreRounding( score , precision = 2 ):
	if score == None: return 0
	return int(score) if float(score) - int(score) < 0.01 or precision == 0 else round(float(score),precision)
def GetArgsAsString(ignore=[]):
	arg = ""
	for key,value in request.args.items():
		if key in ignore: continue
		if arg != "": arg += "&"
		arg += "%s=%s" % (escape(key),escape(value))
	return arg

def CheckPrivilege(username,privileges):
	def Have(username,privilege):
		return db.Execute('SELECT COUNT(*) FROM user_privileges WHERE username=%s AND privilege=%s',(username,privilege))[0]['COUNT(*)'] >= 1
	if username == None: return False
	if isinstance(privileges,str):
		privileges = [privileges]
	privileges.append('system_admin')
	for privilege in privileges:
		if Have(username,privilege):
			return True
	return False
def CheckPrivilegeOfProblem(username,problem_id):
	ok_privileges = ['problemset_manager']
	problems = db.Execute('SELECT provider FROM problems WHERE id=%s',problem_id)
	if len(problems) == 0:
		return False
	problem_provider = problems[0]['provider']
	if problem_provider == username:
		ok_privileges.append('problem_owner')
	return CheckPrivilege(username,ok_privileges)
def CheckPrivilegeOfCode(username,submission_id):
	if config.config['security']['can_view_code'] == True:
		return True
	submissions = db.Execute('SELECT submitter,problem_id FROM submissions WHERE id=%s',submission_id)
	if len(submissions) == 0:
		return False
	submitter = submissions[0]['submitter']
	if submitter == username:
		return True
	return False

def ReturnJSON(data):
	return Response(json.dumps(data),mimetype='application/json')
def RedirectBack( error_message = None , ok_message = None ):
	if error_message != None:
		flash(error_message,'error')
	if ok_message != None:
		flash(ok_message,'ok')
	url = request.referrer
	if url == None or ( request.method == 'GET' and url == request.url ): url = '/'
	return redirect(url)

def ParseInt( s , default = 0 , limit_l = int(-1e9) , limit_r = int(1e9) ):
	if s == None or not s.isdigit(): return default
	try:
		s = int(s)
		if s < limit_l or s > limit_r: return default
		return s
	except:
		return default
def GetCurrentPage():
	return ParseInt(request.args.get('page'),1,1,1e9)

def IsVaildUsername(username):
	if len(username) == 0 or len(username) > 15:
		return False
	banned_chars = ['\n','\r',' ','\b','\t','<','>','/','\\','\'','"','&','#','?','%','$','#','@','!','(',')','[',']','{','}']
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
