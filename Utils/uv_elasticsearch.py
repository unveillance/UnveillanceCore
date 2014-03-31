import json, requests

from conf import HOST, ELS_PORT

class UnveillanceElasticsearch(object):
	def __init__(self):
		print "Initing Elasticsearch handler..."
		
	def get(self, _id):
		print "getting thing"
		
		res = self.sendELSRequest(endpoint=_id)
		try:
			if res['exists']: return res['_source']
		except KeyError as e: pass
		
		return None
	
	def query(self, args):
		print "OH A QUERY"
	
	def sendELSRequest(self, data=None, endpoint=None, method="get"):
		url = "http://%s:%d/unveillance/documents/" % (HOST, ELS_PORT)
		if endpoint is not None:
			url += endpoint
		
		if data is not None:
			data = json.dumps(data)
		
		
		try:
			r = requests.get(url, data=data)
			return json.loads(r.content)

		except Exception as e: print e		
		return None