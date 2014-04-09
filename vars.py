from collections import namedtuple

EmitSentinel = namedtuple("EmitSentinel", "attr type s_replace")
AnnexDescriptor = namedtuple("AnnexDescriptor", "farm p22 p8888")


asset_tags = namedtuple("asset_tags", "ORIG F_MD")
AssetTags = asset_tags("original_document", "metadata_fingerprint")

uv_doc_type = namedtuple("uv_doc_type", "TASK DOC TEXT UVSCRIPT")
UVDocType = uv_doc_type("UV_TASK", "UV_DOCUMENT", "UV_TEXT", "UV_SCRIPT")

MIME_TYPES = {
	'txt' : "text/plain",
	'zip' : "application/zip",
	'image' : "image/jpeg",
	'wildcard' : "application/octet-stream",
	'pgp' : "application/pgp",
	'gzip' : "application/x-gzip",
	'json' : "application/json"
}

MIME_TYPE_MAP = {
	'text/plain' : "txt",
	'application/zip' : "zip",
	'image/jpeg' : "jpg",
	'application/octet-stream' : "wildcard",
	'application/pgp' : "pgp",
	'application/x-gzip' : "gzip",
	'application/json' : "json"
}

class Result(object):
	def __init__(self):
		self.result = 404

	def emit(self): return self.__dict__