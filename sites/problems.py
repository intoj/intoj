# coding: utf-8
from flask import *
from werkzeug import secure_filename
import json, os, random
import HTMLParser
import config, db, modules, static, submissions

def GetProblemInfo(problem_id):
	res = db.Execute('SELECT * FROM problems WHERE id=%s',problem_id)
	if len(res) == 0: return None
	res = res[0]
	def F(s): return '' if s == None else s.decode('utf-8')
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

def SubmitRun(problem_id):
	return modules.ReturnJSON(submissions.NewSubmission(
		problem_id = problem_id
	))

def ProblemListRun():
	per_page = config.config['site']['per_page']['problem_list']
	current_page = modules.GetCurrentPage()
	total_page = (db.Execute('SELECT COUNT(*) FROM problems')[0]['COUNT(*)']+per_page-1) / per_page;
	problems = db.Execute('SELECT id,title,is_public FROM problems LIMIT %s OFFSET %s',
							(per_page,per_page*(current_page-1)))
	nowuser = modules.GetCurrentOperator()
	if nowuser != None:
		for problem in problems:
			latest_submission = db.Execute('SELECT * FROM submissions WHERE submitter=%s AND problem_id=%s AND status != %s \
											ORDER BY status DESC, score DESC, submit_time ASC \
											LIMIT 1',
											(nowuser,problem['id'],static.name_to_id['Skipped']))
			if len(latest_submission) == 0: continue
			problem['submission'] = latest_submission[0]
	return render_template('problemlist.html',problems=problems,pageinfo={ 'per': per_page, 'tot': total_page })

def ProblemRun(problem_id):
	probleminfo = GetProblemInfo(problem_id)
	if probleminfo == None:
		return modules.RedirectBack(error_message='无此题目')
	probleminfo['examples'] = GetProblemExamples(problem_id)
	return render_template('problem.html',problem=probleminfo,languages=config.config['languages'])

def ProblemTestdataDownloadRun(problem_id):
	filename = request.args['path']
	if not modules.IsSafeFilePath(filename):
		return "不安全的文件名"
	testdata_path = os.path.join(config.config['data_path'],str(problem_id))
	return send_from_directory(testdata_path,filename,as_attachment=True)

def ProblemTestdataPreviewRun(problem_id):
	filename = request.args['path']
	if not modules.IsSafeFilePath(filename):
		return "不安全的文件名"
	testdata_path = os.path.join(config.config['data_path'],str(problem_id))
	filepath = os.path.join(testdata_path,filename)
	filesize = os.path.getsize(filepath)/1000
	if filesize > config.config['limits']['max_testdata_preview_size_kb']:
		return "文件过大（限制为 %d KB，实际大小为 %d KB）。请尝试下载。<br />QAQ" % (config.config['limits']['max_testdata_preview_size_kb'],filesize)
	return Response(open(filepath).read(),mimetype='text/plain')
