import json

from conf import HOST

class UnveillanceElasticsearch():
	def __init__(self):
		print "Initing Elasticsearch handler..."
		
	def get(self, _id):
		print "getting thing"
		if not self.status: return None
		
		res = self.sendELSRequest(endpoint=_id)
		try:
			if res['exists']: return res['_source']
		except KeyError as e: pass
		
		return None
	
	def query(self, args):
		print "OH A QUERY"
	
	def update(self, _id, args):
		print "updating thing"
		if not self.status: return False
		
		res = self.sendELSRequest(endpoint=_id, data=args, method="put")

		try: return res['ok']
		except KeyError as e: pass
		
		return False
	
	def create(self, _id, args):
		print "creating thing"
		return self.update(_id, args)
	
	def sendELSRequest(self, data=None, endpoint=None):
		url = "http://%s:9200/unveillance/documents/" % HOST
		if endpoint is not None:
			url += endpoint
		
		if data is not None:
			data = json.dumps(data)
		
		if method == "get":
			r = requests.get(url, data=data)
		elif method == "put":
			r = requests.post(url, data=data)
		elif method == "delete":
			r = requests.delete(url, data=data)
		
		return json.loads(r.content)