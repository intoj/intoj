import pymysql
import config

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
