from redis import StrictRedis
import config

def NewConnection():
	return StrictRedis(host=config.config['redis']['host'], port=config.config['redis']['port'], db=0, password=config.config['redis']['pass'])
