#coding:utf-8
from flask import *
import json
import db, modules, config

def GetProblemInfo(problem_id):
	res = db.Execute('SELECT * FROM problems WHERE id=%s',problem_id)
	if len(res) == 0: return None
	res = res[0]
	def F(s): return '' if s == None else s
	return {
		'id': int(problem_id),
		'title': res['title'],
		'background': F(res['background']),
		'description': F(res['description']),
		'input_format': F(res['input_format']),
		'output_format': F(res['output_format']),
		'limit_and_hint': F(res['limit_and_hint']),
		'time_limit': int(res['time_limit']),
		'memory_limit': int(res['memory_limit']),
		'is_public': bool(res['is_public']),
		'provider': res['provider']
	}
def GetProblemExamples(problem_id):
	res = db.Execute('SELECT kth,input,output,explanation FROM problem_examples WHERE problem_id=%s ORDER BY kth ASC',problem_id)
	return res

def ProblemListRun():
	per_page = config.config['site']['per_page']['problem_list']
	current_page = modules.GetCurrentPage()
	problems = db.Execute('SELECT id,title,is_public FROM problems LIMIT %s OFFSET %s',(per_page,per_page*(current_page-1)))
	return render_template('problemlist.html',problems=problems,current_page=current_page)

def ProblemRun(problem_id):
	probleminfo = GetProblemInfo(problem_id)
	if probleminfo == None:
		return modules.RedirectBack(error_message='无此题目')
	probleminfo['examples'] = GetProblemExamples(problem_id)
	return render_template('problem.html',problem=probleminfo)

def ProblemAddRun():
	operator = modules.GetCurrentOperator()
	if not modules.CheckPrivilege(operator,['prblemset_manager','problem_owner']):
		return modules.RedirectBack(error_message='无此权限')
	if request.method == 'GET':
		return render_template('problemadd.html')
	else:
		id = db.Execute('SELECT MAX(id) FROM problems')[0]['MAX(id)']
		id = 1 if id == None else int(id)+1
		default_time_limit = config.config['default']['problem']['time_limit']
		default_memory_limit = config.config['default']['problem']['memory_limit']
		db.Execute('INSERT INTO problems(id,title,provider,time_limit,memory_limit) VALUES(%s,%s,%s,%s,%s)',(id,request.form['title'],operator,default_time_limit,default_memory_limit))
		return redirect('/problem/%d'%id)

def ProblemEditRun(problem_id):
	operator = modules.GetCurrentOperator()
	probleminfo = GetProblemInfo(problem_id)
	if probleminfo == None:
		return modules.RedirectBack(error_message='无此题目')
	probleminfo['examples'] = GetProblemExamples(problem_id)

	if not modules.CheckPrivilegeOfProblem(operator,problem_id):
		return modules.RedirectBack(error_message='无此权限')
	if request.method == 'GET':
		return render_template('problemedit.html',problem=probleminfo)
	else:
		new_problem_id = int(request.form['new_problem_id'])
		if new_problem_id != problem_id:
			is_duplicate = db.Execute('SELECT COUNT(*) FROM problems WHERE id=%s',new_problem_id)[0]['COUNT(*)']
			if is_duplicate:
				return modules.ReturnJSON({ 'success': False, 'message': '新 id 已存在' })
		db.Execute('UPDATE problems SET id=%s, title=%s, background=%s, \
					description=%s, input_format=%s, output_format=%s, \
					limit_and_hint=%s, is_public=%s WHERE id=%s',
					(new_problem_id,
					request.form['new_title'],
					request.form['new_background'],
					request.form['new_description'],
					request.form['new_input_format'],
					request.form['new_output_format'],
					request.form['new_limit_and_hint'],
					request.form['new_is_public'],
					problem_id))
		examples = json.loads(request.form['examples'])
		db.Execute('DELETE FROM problem_examples WHERE problem_id=%s',problem_id)
		now_kth = 0
		for example in examples:
			now_kth += 1
			db.Execute('INSERT INTO problem_examples(problem_id,kth,input,output,explanation) VALUE(%s,%s,%s,%s,%s)',
					   (new_problem_id,now_kth,example['input'],example['output'],example['explanation']))
		return modules.ReturnJSON({ 'success': True, 'message': '提交成功！' })

def ProblemDeleteRun(problem_id):
	operator = modules.GetCurrentOperator()
	if not modules.CheckPrivilegeOfProblem(operator,problem_id):
		return modules.RedirectBack(error_message='无此权限')
	db.Execute('DELETE FROM problems WHERE id=%s',problem_id)
	flash('成功删除题目 #%d'%problem_id,'ok')
	return redirect('/problems')
