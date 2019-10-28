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

def GetParameters(args,allow_parameters):
	result_string = ''
	result_list = []
	for key, value in args.items():
		if key not in allow_parameters or modules.IsEmpty(value): continue
		try:
			if allow_parameters[key]['checker'](value) == False:
				continue
		except:
			continue
		if result_string == '': result_string += 'WHERE '
		else: result_string += ' AND '
		result_string += allow_parameters[key]['parameter']
		result_list.append(value)
	return result_string, result_list
def ExecuteWithParameters(cmd,args_dict,allow_parameters,arg_list=['PARAMETERS']):
	arg_list = list(arg_list)
	parameter_string, parameter_arg = GetParameters(args_dict,allow_parameters)
	cmd = cmd.format( PARAMETERS = parameter_string )
	arg_list = arg_list[:arg_list.index('PARAMETERS')] + parameter_arg + arg_list[arg_list.index('PARAMETERS')+1:]
	# print(cmd,arg_list)
	return Execute(cmd,arg_list)
