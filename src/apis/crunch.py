# -*- coding: utf-8 -*-

"""
try:
	from urllib import urlencode
except:
	from urllib.parse import urlencode

try:
	from urllib2 import urlopen
except:
	from urllib.request import urlopen

import json

API_URL = "http://api.crunchbase.com/v/2/"

class CrunchBase(object):
	
	def _request(self, endpoint, data, method="POST", _id=None):
		if method in ["GET"]:
			if _id:
				return json.loads(urlopen("%s%s/%s?%s" % (API_URL, endpoint, _id, urlencode(data))).read().decode('utf-8'))
			else:
				return json.loads(urlopen("%s%s?user_key=%s&%s" % (API_URL, endpoint, self.access_token, urlencode(data))).read().decode('utf-8'))
		if not self.access_token:
			return {'error':'No access token'}
		return json.loads(urlopen("%s%s?user_key=%s&%s" % (API_URL, endpoint, self.access_token, urlencode(data))).read().decode('utf-8'))

	def __init__(self, access_token = None):
		self.access_token	= access_token

	def __getattr__(self, name):
		def wrapper(data):
			_id = None
			if 'method' in data:
				method = data['method'] 
				del data['method']
			else:
				method = "POST"
			if 'id' in data:
				_id=data['id']
				del data['id']
			return self._request(name.replace("__","/"), data, method, _id)
		return wrapper
"""

import json
import requests
try:
	from urllib import urlencode
except:
	from urllib.parse import urlencode


API_URL = "http://api.crunchbase.com/v/2/"

class CrunchBase(object):


	def _request(self, endpoint, data, method="POST", _id=None):
		if _id:
			id_part = "/" + _id
		else:
			id_part = ""
		url = API_URL + endpoint + id_part + "/?user_key=" + self.access_token + "&%s"%(urlencode(data))
		res = requests.get(url)
		return json.loads(res.text)

	def __init__(self, access_token = None):
		self.access_token	= access_token

	def __getattr__(self, name):
		def wrapper(data):
			_id = None
			if 'method' in data:
				method = data['method'] 
				del data['method']
			else:
				method = "POST"
			if 'id' in data:
				_id=data['id']
				del data['id']
			return self._request(name.replace("__","/"), data, method, _id)
		return wrapper







