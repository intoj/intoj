#coding:utf-8
from flask import *
import db, modules, config

def SubmissionListRun():
	per_page = config.config['site']['per_page']['submission_list']
	current_page = modules.GetCurrentPage()
	total_page = (db.Execute('SELECT COUNT(*) FROM submissions')[0]['COUNT(*)']+per_page-1) / per_page;
	submissions = db.Execute('SELECT id,problem_id,contest_id,submitter,submit_time,language,status,score,time_usage,memory_usage FROM submissions ORDER BY id DESC LIMIT %s OFFSET %s',
							 (per_page,per_page*(current_page-1)))
	return render_template('submissionlist.html',submissions=submissions,pageinfo={ 'per': per_page, 'tot': total_page })

# statics

def GetColorOfScore(a,fullscore=100):
	a = float(a)
	fullscore = float(fullscore)
	if a <= fullscore/2:
		g = int( (a/fullscore) * (255+255-80) )
		return "rgb(255,%d,0)" % g
	else:
		r = int( (1.0-a/fullscore) * (255+255) )
		return "rgb(%d,220,0)" % r

id_to_word = {
	0: 'Running',
	1: 'Waiting',
	2: 'Judgement Failed',
	3: 'Compile Error',
	4: 'Hacked',
	5: 'Wrong Answer',
	6: 'Output Limit Exceeded',
	7: 'Time Limit Exceeded',
	8: 'Memory Limit Exceeded',
	9: 'Runtime Error',
	10: 'Partially Accepted',
	11: 'Accepted'
}
id_to_sign = {
	0: 'fa fa-fw fa-spinner fa-spin',
	1: 'fa fa-fw fa-spinner fa-spin',
	2: 'fa fa-fw fa-smile-o',
	3: 'fa fa-fw fa-code',
	4: 'fa fa-fw fa-smile-o',
	5: 'fa fa-fw fa-times',
	6: 'fa fa-fw fa-snowflake-o',
	7: 'fa fa-fw fa-clock-o',
	8: 'fa fa-fw fa-microchip',
	9: 'fa fa-fw fa-exclamation',
	10: 'fa fa-fw fa-adjust',
	11: 'fa fa-fw fa-check'
}
id_to_color = {
	0: '#66ccff',
	1: '#aaa',
	2: '#ff0000',
	3: '#ede42b',
	4: '#ee0000',
	5: '#ff4444',
	6: 'orange',
	7: 'orange',
	8: 'orange',
	9: 'purple',
	10: '#19d960',
	11: '#1eff1e'
}
