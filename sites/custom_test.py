# coding: utf-8
from flask import *
import config, db, modules, static, submissions

def CustomTestRun():
	if request.method == 'GET':
		return render_template('custom-test.html')
	else:
		input_data = request.form['input_data']
		if len(input_data) > config.config['limits']['max_custom_test_input_length']*1024:
			return modules.ReturnJSON({ 'success': False , 'message': '输入数据过长（长度限制为 %d KB）'%config.config['limits']['max_custom_test_input_length']})
		result = submissions.NewSubmission( type = 'custom_test' )
		if result['success'] == False:
			return modules.ReturnJSON(result)
		id = result['submission_id']
		db.Execute('INSERT INTO custom_tests(id,input) VALUES(%s,%s)',(id,input_data))
		return modules.ReturnJSON(result)
