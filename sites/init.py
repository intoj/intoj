from flask import *
import config

def Init():
	if session.get('inited') == None:
		session['client_keys'] = {}
		session['inited'] = 'inited'
