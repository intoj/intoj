# coding: utf-8
from flask import *
from werkzeug import secure_filename
import json, os, random
import HTMLParser
import config, db, modules, static, submissions, problems

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
	probleminfo = problems.GetProblemInfo(problem_id)
	if probleminfo == None:
		return modules.RedirectBack(error_message='无此题目')
	probleminfo['examples'] = problems.GetProblemExamples(problem_id)

	if request.method == 'GET':
		return render_template('problemedit.html',problem=probleminfo)
	else:
		new_problem_id = int(request.form['new_problem_id'])
		if new_problem_id != problem_id:
			if new_problem_id <= 0:
				return modules.ReturnJSON({ 'success': False, 'message': 'id 必须是正整数' })
			is_duplicate = db.Execute('SELECT COUNT(*) FROM problems WHERE id=%s',new_problem_id)[0]['COUNT(*)']
			if is_duplicate:
				return modules.ReturnJSON({ 'success': False, 'message': '新 id 已存在' })
			os.system('mv %s %s'%
						(os.path.join(config.config['data_path'],str(problem_id)),
						os.path.join(config.config['data_path'],str(new_problem_id)))
					)
			db.Execute('UPDATE submissions SET problem_id=%s WHERE problem_id=%s',(new_problem_id,problem_id))

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
			if modules.IsEmpty(example['input']) and modules.IsEmpty(example['output']) and modules.IsEmpty(example['explanation']):
				continue
			now_kth += 1
			db.Execute('INSERT INTO problem_examples(problem_id,kth,input,output,explanation) VALUE(%s,%s,%s,%s,%s)',
					   (new_problem_id,now_kth,example['input'],example['output'],example['explanation']))
		return modules.ReturnJSON({ 'success': True, 'message': '提交成功！' })

def ProblemDeleteRun(problem_id):
	operator = modules.GetCurrentOperator()
	if not modules.CheckPrivilegeOfProblem(operator,problem_id):
		return modules.RedirectBack(error_message='无此权限')

	db.Execute('DELETE FROM problems WHERE id=%s',problem_id)
	db.Execute('DELETE FROM submissions WHERE problem_id=%s',problem_id)
	os.system('rm -rf %s'%os.path.join(config.config['data_path'],str(problem_id)))
	flash('成功删除题目 #%d'%problem_id,'ok')
	return redirect('/problems')

def ProblemManageRun(problem_id):
	operator = modules.GetCurrentOperator()
	if not modules.CheckPrivilegeOfProblem(operator,problem_id):
		return modules.RedirectBack(error_message='无此权限')
	problem = problems.GetProblemInfo(problem_id)
	if problem == None:
		return modules.RedirectBack(error_message='无此题目')

	testdata_path = os.path.join(config.config['data_path'],str(problem_id))
	if request.method == 'GET':
		try: problem['data_config'] = open(os.path.join(testdata_path,'config.json'),'r').read()
		except: problem['data_config'] = ''
		def ListFiles(testdata_path,path):
			all_items = os.listdir(path)
			files = []
			for filename in all_items:
				filepath = os.path.join(path,filename)
				if os.path.isdir(filepath):
					files.append({
						'type': 'dir',
						'name': filename,
						'path': filepath.replace(testdata_path+'/',''),
						'files': ListFiles(testdata_path,filepath)
					})
				else:
					files.append({
						'type': 'file',
						'name': filename,
						'path': filepath.replace(testdata_path+'/','')
					})
			return sorted(files,key = lambda x: '' if x['name'] == 'config.json' else x['name'])
		files = {
			'type': 'root_dir',
			'name': '/',
			'path': '.',
			'files': ListFiles(testdata_path,testdata_path)
		}
		problem['files'] = files
		return modules.render_template('problemmanage.html',problem=problem)
	else:
		if request.form['type'] == 'data_upload':
			config_detail = request.form['new_data_config']
			open(os.path.join(testdata_path,'config.json'),'w').write(config_detail)
			try:
				_tmp = json.loads(config_detail)
			except BaseException as exception:
				flash('json 格式有误: %s'%exception,'error')
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
