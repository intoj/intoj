#coding:utf-8
from flask import *
import config, db, modules, static

def AdminHomeRun():
	operator = modules.GetCurrentOperator()
	if not modules.CheckPrivilege(operator,'system_admin'):
		return modules.RedirectBack('无此权限')
	return render_template('admin.html')

def AdminRejudgeRun():
	operator = modules.GetCurrentOperator()
	if not modules.CheckPrivilege(operator,'system_admin'):
		return modules.RedirectBack('无此权限')
	return render_template('admin_rejudge.html')
