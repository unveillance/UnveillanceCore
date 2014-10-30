from re import compile
from collections import namedtuple

EmitSentinel = namedtuple("EmitSentinel", "attr type s_replace")
AnnexDescriptor = namedtuple("AnnexDescriptor", "farm p22 p8888")
SubDescriptor = namedtuple('SubDescriptor', 'regex sub')

ALLOWED_DATA_ROOTS = [".data", ".synctasks/local"]
UV_DOC_TYPE = {
	'TASK' : "UV_TASK",
	'DOC' : "UV_DOCUMENT",
	'SCRIPT' : "UV_SCRIPT"
}

ASSET_TAGS = {
	'TXT_JSON' : "text_json",
	'KW' : "keywords",
	'BOW' : "bag_of_words",
	'F_MD' : "metadata_fingerprint"
}

MIME_TYPES = {
	'txt' : "text/plain",
	'json' : "application/json",
	'symlink' : "inode/symlink",
	'txt_stub' : "unveillance/textstub"
}

MIME_TYPE_MAP = {
	'text/plain' : "txt",
	'application/json' : "json",
	'inode/symlink' : "symlink",
	'unveillance/textstub' : "txt_stub"
}

MIME_TYPE_TASKS = {
	'text/plain' : [
		'Text.evaluate_text.evaluateText'
	],
	'inode/symlink' : [
		'Document.pull_from_annex.pullFromAnnex'
	]
}

METADATA_ASPECTS = {}

UNCAUGHT_UNICODES = [SubDescriptor(u'\u2014', "--"),
	SubDescriptor(u'\u0152', "oe"),
	SubDescriptor(u'\u2122', "'"),
	SubDescriptor(u'\ufb01', "\""),
	SubDescriptor(u'\ufb02', "\""),
	SubDescriptor(u'\u2013', "--"),
	SubDescriptor(u'\u0160', "S"),
	SubDescriptor(u'\u201a', ",")
	]

UNCAUGHT_PUNCTUATION = [SubDescriptor(r'\.', None),
	SubDescriptor(r',', None),
	SubDescriptor(r'"', None),
	SubDescriptor(r'\?', None),
	SubDescriptor(r'\&', "and"),
	SubDescriptor(r':', None),
	SubDescriptor(r';', None),
	SubDescriptor(r'\-', None),
	SubDescriptor(r'\n', None),
	SubDescriptor(r'\]|\[', None),
	SubDescriptor(r'\(|\)', None),
	SubDescriptor(r'<|>', None),
	SubDescriptor(r'\!', None)]

SPLITTERS = compile(' |\-\-|&')

STOPWORDS = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves',
	'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 
	'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 
	'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 
	'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 
	'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 
	'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 
	'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 
	'between', 'into', 'through', 'during', 'before', 'after', 'above', 
	'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 
	'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 
	'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 
	'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 
	'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 
	'don', 'should', 'now']

class Result(object):
	def __init__(self):
		self.result = 404

	def emit(self): return self.__dict__