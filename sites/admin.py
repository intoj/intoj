# coding: utf-8
from flask import *
import config, db, modules, static

def AdminHomeRun():
	operator = modules.GetCurrentOperator()
	if not modules.CheckPrivilege(operator,'system_admin'):
		return modules.RedirectBack('无此权限')

	statistic_datas = {
		'problems_count': db.Execute('SELECT COUNT(*) FROM problems')[0]['COUNT(*)'],
		'submissions_count': db.Execute('SELECT COUNT(*) FROM submissions')[0]['COUNT(*)'],
		'users_count': db.Execute('SELECT COUNT(*) FROM users')[0]['COUNT(*)']
	}

	system_infos = {}
	try:
		with open('.git/FETCH_HEAD','r') as f:
			system_infos['version_number'] = f.readline().split()[0]
	except:
		pass
	return render_template('admin.html',statistic_datas=statistic_datas,system_infos=system_infos)

def AdminRejudgeRun():
	operator = modules.GetCurrentOperator()
	if not modules.CheckPrivilege(operator,'system_admin'):
		return modules.RedirectBack('无此权限')
	return render_template('admin_rejudge.html')
