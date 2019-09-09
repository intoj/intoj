#coding:utf-8
from flask import *
import db, modules, config

def GetProblemInfo(problem_id):
	res = db.Execute('SELECT * FROM problems WHERE id=%s',problem_id)
	if len(res) == 0: return None
	res = res[0]
	return {
		'id': int(problem_id),
		'title': res['title'],
		'background': res['background'],
		'description': res['description'],
		'input_format': res['input_format'],
		'output_format': res['output_format'],
		'limit_and_hint': res['limit_and_hint'],
		'time_limit': int(res['time_limit']),
		'memory_limit': int(res['memory_limit']),
		'is_public': bool(res['is_public'])
	}

def ProblemListRun():
	per_page = config.config['site']['per_page']['problem_list']
	current_page = modules.ParseInt(request.args.get('page'),1,1,1e9)
	problems = db.Execute('SELECT * FROM problems LIMIT %s OFFSET %s',(per_page,per_page*(current_page-1)))
	return render_template('problemlist.html',problems=problems,current_page=current_page)

def ProblemRun(problem_id):
	probleminfo = GetProblemInfo(problem_id)
	return render_template('problem.html',problem=probleminfo)
