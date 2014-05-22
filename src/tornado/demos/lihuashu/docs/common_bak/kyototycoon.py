import time
import urllib
import platform

if platform.python_version()== "2.7.3":
	from httplib2 import httplib as http_client
	from urllib import quote as urllib_parse_quote
else:
	import http.client as http_client
	from urllib.parse import quote as urllib_parse_quote

# RESTful interface of Kyoto Tycoon
# By Insion
'''KEY=main;sub not main:sub'''

class KyotoTycoon:
	# connect to the server
	def open(self, host = "127.0.0.1", port = 1978, timeout = 30):
		try:
			self.ua = http_client.HTTPConnection(host, port, False, timeout)
			return True
		except:
			return None

	# close the connection
	def close(self):
		try:
			self.ua.close()
			return True
		except:
			return None

	# store a record
	def set(self, key, value, xt = None):
		if key==None or key=='' or key==b'' or value==None or value=='' or value==b'':
			return None
		else:
			if isinstance(key, str): key = key.encode("utf8")
			if isinstance(value, str): value = value.encode("utf8")
			key = "/" + urllib_parse_quote(key)

			headers = {}
			if xt != None:
				xt = int(time.time()) + xt
				headers["X-Kt-Xt"] = str(xt)

			self.ua.request("PUT", key, value, headers)
			res = self.ua.getresponse()
			body = res.read()
			return res.status == 201

	def set_int(self, key, value, xt = None):
		self.set(key,str(value), xt)

	# remove a record
	def remove(self, key):
		if isinstance(key, str): key = key.encode("utf8")
		key = "/" + urllib_parse_quote(key)
		self.ua.request("DELETE", key)
		res = self.ua.getresponse()
		body = res.read()
		return res.status == 204

	# retrieve the value of a record
	def get(self, key):
		if key==None or key=="" or key==b"":
			return None
		else:
			if isinstance(key, str): key = key.encode("utf8")
			key = "/" + urllib_parse_quote(key)

			self.ua.request("GET", key)
			res = self.ua.getresponse()
			body = res.read()
			if res.status != 200:
				return None
			else:
				return body

	def get_int(self, key):
		if self.get(key) ==None:
			return None
		else:
			return int(str(self.get(key),'utf8'))

	def get_str(self, key):
		if self.get(key) ==None:
			return None
		else:
			return str(self.get(key),'utf8')



'''
# sample usage
kt = KyotoTycoon()
kt.open("localhost", 1978)
kt.set("japan", "tokyo", 60)
print(kt.get("japan"))
kt.remove("japan")
kt.close()
'''