#coding:utf-8
from flask import *
import sys,os,time
reload(sys)
sys.dont_write_bytecode = True
sys.setdefaultencoding('utf-8')
workpath = os.path.dirname(os.path.abspath('app.py'))
sitespath = os.path.join(workpath,'sites')
if sitespath not in sys.path: sys.path.insert(0,sitespath)
import sites

app = Flask('intoj')
sites.config.ReadFromFile('config.json')
app.secret_key = sites.config.config['site']['secret_key']

app.add_template_global(min,'min')
app.add_template_global(max,'max')
app.add_template_global(len,'len')

app.add_template_global(sites.config.config,'config')
app.add_template_global(sites.db.Execute,'dbExecute')
app.add_template_global(sites.modules.IsEmpty,'IsEmpty')
app.add_template_global(sites.modules.GetGravatarEmailHash,'GetGravatarEmailHash')
app.add_template_global(sites.modules.GetGravatarAddress,'GetGravatarAddress')
app.add_template_global(sites.modules.GetCurrentOperator,'GetCurrentOperator')
app.add_template_global(sites.modules.ValidatePassword,'ValidatePassword')
app.add_template_global(sites.modules.ValidateClientkey,'ValidateClientkey')

@app.route('/')
def Index():
	return sites.index.Run()

@app.route('/register',methods=['GET','POST'])
def Register():
	return sites.register.Run()

@app.route('/login',methods=['GET','POST'])
def Login():
	return sites.login.Run()

@app.route('/problems')
def ProblemList():
	return sites.problems.ProblemListRun()

@app.route('/problem/<int:problem_id>')
def Problem(problem_id):
	return sites.problems.ProblemRun(problem_id)

@app.route('/users')
def UserList():
	return sites.users.UserListRun()

@app.route('/user/<string:username>')
def UserHome(username):
	return sites.users.UserHomeRun(username)

@app.route('/user/<string:username>/edit',methods=['GET','POST'])
def UserEdit(username):
	return sites.users.UserEditRun(username)
