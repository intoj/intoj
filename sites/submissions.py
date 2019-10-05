#coding:utf-8
from flask import *
import datetime, json
import db, modules, config, reedis

def SubmissionListRun():
	per_page = config.config['site']['per_page']['submission_list']
	current_page = modules.GetCurrentPage()
	total_page = (db.Execute('SELECT COUNT(*) FROM submissions')[0]['COUNT(*)']+per_page-1) / per_page;
	submissions = db.Execute('SELECT id,problem_id,contest_id,submitter,submit_time,language,status,score,time_usage,memory_usage FROM submissions ORDER BY id DESC LIMIT %s OFFSET %s',
							 (per_page,per_page*(current_page-1)))
	return render_template('submissionlist.html',submissions=submissions,pageinfo={ 'per': per_page, 'tot': total_page })

def GetSubmissionInfo(submission_id):
	res = db.Execute('SELECT * FROM submissions WHERE id=%s',submission_id)
	if len(res) == 0: return None
	res = res[0]
	res['length'] = len(res['code'])
	res['detail'] = json.loads(res['detail'])
	return res

def SubmissionRun(submission_id):
	submission_info = GetSubmissionInfo(submission_id)
	if submission_info == None:
		return modules.RedirectBack(error_message='无此提交')
	return render_template('submission.html',submission=submission_info)

'''
intoj 评测流程
1. 当用户发起一发新提交时，前端中 NewSubmission() 将会把此次评测的相关信息写入数据库，并将 submission_id 扔到 redis 队列 intoj-waiting-judge 内
2. 评测后端轮询 redis 队列 intoj-waiting-judge，当有新的 submission_id 时便开始评测
3. 评测后端一旦要变更 submission 信息，就会更新数据库，同时把 submission_id 放进 redis 队列 intoj-judgestatus-refreshed 内
4. 前端轮询 redis 队列 intoj-judgestatus-refreshed，若有变更就通过 websocket 告知客户端
5. 客户端进行相应处理
'''
def NewSubmission(problem_id,contest_id=0):
	code, language = request.form['code'], request.form['lang']
	submitter = modules.GetCurrentOperator()
	submit_time = datetime.datetime.now().strftime('%Y.%m.%d %H:%M:%S')

	if submitter == None:
		return modules.ReturnJSON({ 'success': False, 'message': '请先登录' })
	if len(code.strip()) == 0:
		return modules.ReturnJSON({ 'success': False, 'message': '你这么短？emmm....' })
	if len(code) > config.config['limits']['max_code_length']*1024:
		return modules.ReturnJSON({ 'success': False, 'message': '代码过长（代码长度限制为 %d KB）'%config.config['limits']['max_code_length'] })

	id = db.Execute('SELECT MAX(id) FROM submissions')[0]['MAX(id)']
	id = 1 if id == None else int(id)+1
	db.Execute('INSERT INTO submissions(id,problem_id,contest_id,submitter,submit_time,language,code,detail) VALUES(%s,%s,%s,%s,%s,%s,%s,"{}")',
				(id,problem_id,contest_id,submitter,submit_time,language,code))

	redis = reedis.NewConnection()
	redis.rpush('intoj-waiting-judge',id)

	return modules.ReturnJSON({ 'success': True, 'message': '提交成功', 'submission_id': id })

def SubmissionRejudgeRun(submission_id):
	submission_info = GetSubmissionInfo(submission_id)
	operator = modules.GetCurrentOperator()
	if submission_info == None:
		return modules.ReturnJSON({ 'success': False, 'message': '无此提交'})
	if not modules.CheckPrivilegeOfProblem(operator,submission_info['problem_id']):
		return modules.ReturnJSON({ 'success': False, 'message': '无此权限'})

	db.Execute('UPDATE submissions SET status=1 WHERE id=%s',submission_id)

	redis = reedis.NewConnection()
	redis.rpush('intoj-waiting-rejudge',submission_id)

	return modules.ReturnJSON({ 'success': True, 'message': '成功重测' })

def SubmissionDeleteRun(submission_id):
	submission_info = GetSubmissionInfo(submission_id)
	operator = modules.GetCurrentOperator()
	if submission_info == None:
		return modules.ReturnJSON({ 'success': False, 'message': '无此提交'})
	if not modules.CheckPrivilegeOfProblem(operator,submission_info['problem_id']):
		return modules.ReturnJSON({ 'success': False, 'message': '无此权限'})

	db.Execute('DELETE FROM submissions WHERE id=%s',submission_id)
	return modules.ReturnJSON({ 'success': True, 'message': '成功删除' })
