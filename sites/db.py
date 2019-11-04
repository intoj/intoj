# coding: utf-8
import pymysql
import config, modules

def GetConnection():
	db_name = config.config['database']['name']
	db_user = config.config['database']['user']
	db_host = config.config['database']['host']
	db_pass = config.config['database']['pass']
	db = pymysql.connect(db_host,db_user,db_pass,db_name)
	cur = db.cursor(cursor=pymysql.cursors.DictCursor)
	return db,cur
def CloseConnection(db,cur):
	cur.close()
	db.close()

def Execute(cmd,arg=None):
	db,cur = GetConnection()
	if arg == None: cur.execute(cmd)
	else: cur.execute(cmd,arg)
	command_name = cmd.split()[0]
	if command_name not in ['SELECT']:
		db.commit()
	res = cur.fetchall()
	CloseConnection(db,cur)
	return res

def GetFilters(args,allowed_filters):
	result_string = ''
	result_list = []
	for key, value in args.items():
		if key not in allowed_filters or modules.IsEmpty(value): continue
		try:
			if allowed_filters[key]['checker'](value) == False:
				continue
		except:
			continue
		if result_string == '': result_string += 'WHERE '
		else: result_string += ' AND '
		result_string += allowed_filters[key]['filter']
		result_list.append(value)
	return result_string, result_list
def ExecuteWithFilters(cmd,args_dict,allowed_filters,arg_list=['FILTERS']):
	filter_string, filter_arg = GetFilters(args_dict,allowed_filters)
	cmd = cmd.format( FILTERS = filter_string )
	arg_list = list(arg_list)
	arg_list = arg_list[:arg_list.index('FILTERS')] + filter_arg + arg_list[arg_list.index('FILTERS')+1:]
	return Execute(cmd,arg_list)
