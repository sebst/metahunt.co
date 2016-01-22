# -*- coding: utf-8 -*-

try:
	from urllib import urlencode
except:
	from urllib.parse import urlencode

try:
	from urllib2 import urlopen
except:
	from urllib.request import urlopen

import json
import requests

ANGELLIST_API_URL = "https://api.angel.co/1/"
API_URL = ANGELLIST_API_URL


class AngelList(object):
	
	"""
	def _request(self, endpoint, data, method="POST", _id=None):
		if method in ["GET"]:
			if _id:
				return json.loads(urlopen("%s%s/%s?%s" % (ANGELLIST_API_URL, endpoint, _id, urlencode(data))).read().decode('utf-8'))
			else:
				return json.loads(urlopen("%s%s?%s" % (ANGELLIST_API_URL, endpoint, urlencode(data))).read().decode('utf-8'))
		if not self.access_token:
			return {'error':'No access token'}
		return json.loads(urlopen("%s%s?access_token=%s&%s" % (ANGELLIST_API_URL, endpoint, self.access_token, urlencode(data))).read().decode('utf-8'))
	"""
	def _request(self, endpoint, data, method="POST", _id=None):
		if _id:
			id_part = "/" + _id
		else:
			id_part = ""
		url = API_URL + endpoint + id_part + "/?access_token=" + self.access_token + "&%s"%(urlencode(data))
		#print (url)
		res = requests.get(url)
		return json.loads(res.text)



	def __init__(self, access_token = None):
		self.access_token	= access_token

	def __getattr__(self, name):
		def wrapper(data):
			#name = name.replace("__","/")

			_id = None
			if 'method' in data:
				method = data['method'] 
				del data['method']
			else:
				method = "POST"
			if 'id' in data:
				_id=data['id']
				del data['id']

			if "ID" in name and _id is not None:
				_id = str(_id)
				return self._request(name.replace("__","/").replace('ID', _id), data, method, None)
			
			return self._request(name.replace("__","/"), data, method, _id)
		return wrapper