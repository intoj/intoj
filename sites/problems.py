#coding:utf-8
from flask import *
from werkzeug import secure_filename
import json, os
import db, modules, config, random

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

def ProblemTestdataDownloadRun(problem_id):
	filename = secure_filename(request.args['filename'])
	testdata_path = os.path.join(config.config['data_path'],str(problem_id))
	return send_from_directory(testdata_path,filename,as_attachment=True)

def ProblemAddRun():
	operator = modules.GetCurrentOperator()
	if not modules.CheckPrivilege(operator,['problemset_manager','problem_owner']):
		return modules.RedirectBack(error_message='无此权限')

	if request.method == 'GET':
		return render_template('problemadd.html')
	else:
		id = db.Execute('SELECT MAX(id) FROM problems')[0]['MAX(id)']
		id = 1 if id == None else int(id)+1
		default_time_limit = config.config['default']['problem']['time_limit']
		default_memory_limit = config.config['default']['problem']['memory_limit']
		db.Execute('INSERT INTO problems(id,title,provider,time_limit,memory_limit) VALUES(%s,%s,%s,%s,%s)',(id,request.form['title'],operator,default_time_limit,default_memory_limit))
		os.system('mkdir %s'%os.path.join(config.config['data_path'],str(id)))
		return redirect('/problem/%d'%id)

def ProblemEditRun(problem_id):
	operator = modules.GetCurrentOperator()
	if not modules.CheckPrivilegeOfProblem(operator,problem_id):
		return modules.RedirectBack(error_message='无此权限')
	probleminfo = GetProblemInfo(problem_id)
	if probleminfo == None:
		return modules.RedirectBack(error_message='无此题目')
	probleminfo['examples'] = GetProblemExamples(problem_id)

	if request.method == 'GET':
		return render_template('problemedit.html',problem=probleminfo)
	else:
		new_problem_id = int(request.form['new_problem_id'])
		if new_problem_id != problem_id:
			is_duplicate = db.Execute('SELECT COUNT(*) FROM problems WHERE id=%s',new_problem_id)[0]['COUNT(*)']
			if is_duplicate:
				return modules.ReturnJSON({ 'success': False, 'message': '新 id 已存在' })
			os.system('mv %s %s'%
						(os.path.join(config.config['data_path'],str(problem_id)),
						os.path.join(config.config['data_path'],str(new_problem_id)))
					)
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
	os.system('rm -rf %s'%os.path.join(config.config['data_path'],str(problem_id)))
	flash('成功删除题目 #%d'%problem_id,'ok')
	return redirect('/problems')

def ProblemManageRun(problem_id):
	operator = modules.GetCurrentOperator()
	if not modules.CheckPrivilegeOfProblem(operator,problem_id):
		return modules.RedirectBack(error_message='无此权限')
	problem = GetProblemInfo(problem_id)
	if problem == None:
		return modules.RedirectBack(error_message='无此题目')

	testdata_path = os.path.join(config.config['data_path'],str(problem_id))
	if request.method == 'GET':
		try: problem['data_config'] = open(os.path.join(testdata_path,'config.json'),'r').read()
		except: problem['data_config'] = ''
		files = sorted(os.listdir(testdata_path))
		problem['files'] = files
		return modules.render_template('problemmanage.html',problem=problem)
	else:
		if request.form['type'] == 'data_upload':
			open(os.path.join(testdata_path,'config.json'),'w').write(request.form['new_data_config'])
			try:
				_tmp = json.loads(request.form['new_data_config'])
			except:
				flash('json 格式有误','error')
				return redirect('/problem/%d/manage'%problem_id)

			db.Execute('UPDATE problems SET time_limit=%s, memory_limit=%s WHERE id=%s',
						(request.form['new_time_limit'],
						 request.form['new_memory_limit'],
						 problem_id))

			file = request.files['data']
			if file.filename != '':
				if '.' not in file.filename or file.filename.rsplit('.', 1)[1] != 'zip':
					flash('文件格式应为 zip','error')
					return redirect('/problem/%d/manage'%problem_id)
				filename = str(random.randint(1,10)) + '.zip'
				filepath = os.path.join(config.config['session_path'],filename)
				file.save(filepath)

				check_ok = os.system('unzip -t -qq %s'%filepath)
				if check_ok != 0:
					flash('无效的 zip 格式','error')
					return redirect('/problem/%d/manage'%problem_id)

				testdata_path = os.path.join(config.config['data_path'],str(problem_id))
				config_path = os.path.join(testdata_path,'config.json')
				config_bkup_path = os.path.join(config.config['session_path'],'config.json.bkup')
				os.system('cp %s %s'%(config_path,config_bkup_path))
				os.system('rm -rf %s'%testdata_path)
				os.system('mkdir %s'%testdata_path)
				print('Extracting testdata for problem %d...'%problem_id)
				os.system('unzip %s -d %s'%(filepath,testdata_path))
				os.system('cp %s %s'%(config_bkup_path,config_path))

			flash('修改成功','ok')
			return redirect('/problem/%d/manage'%problem_id)
