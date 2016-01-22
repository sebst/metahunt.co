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


API_URL = "http://api.betalist.com/v1/"


class BetaList(object):
	

	def _request(self, endpoint, data, method="POST", _id=None):
		if _id:
			id_part = "/" + _id
		else:
			id_part = ""
		url = API_URL + endpoint + id_part + "/?access_token=" + self.access_token + "&%s"%(urlencode(data))
		print (url)
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