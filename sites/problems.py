#coding:utf-8
from flask import *
import db, modules, config

def GetPorblemInfo(problem_id):
	res = db.Execute('SELECT * FROM problems WHERE problem_id=%s',problem_id)
	if len(res) == 0: return None
	res = res[0]
	return {
		'id': problem_id,
		'title': res['title'],
		'description': res['description'],
		'input_format': res['input_format'],
		'output_format': res['output_format']
	}

def ProblemListRun():
	per_page = config.config['site']['per_page']['problem_list']
	current_page = modules.ParseInt(request.args.get('page'),1,1,1e9)
	problems = db.Execute('SELECT * FROM problems LIMIT %s OFFSET %s',(per_page,per_page*(current_page-1)))
	return render_template('problemlist.html',problems=problems,current_page=current_page)

def ProblemRun():
