# coding: utf-8
import json

config = {}
def ReadFromFile(filename):
	global config
	with open(filename,'r') as config_file:
		s = config_file.read()
		config = json.loads(s)
