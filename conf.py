import hashlib, json, base64

from Crypto.Cipher import AES
from Crypto import Random

def getUserCredentialsFile(username):
	return "%s.txt" % hashlib.sha1(username)

def createNewUser(username, password, credentials, users_root, 
	users_salt, users_iv, as_admin=False):
	
	try:
		credentials['username'] = username
		if as_admin:
			credentials['admin'] = True
		
		cred_file = getUserCredentialsFile(username)

		try:
			with open(os.path.join(users_root, cred_file), 'rb') as CREDS:
				return False
		except IOError as e: pass
		
		with open(os.path.join(users_root, cred_file), 'wb+') as CREDS:
			CREDS.write(encrypt(credentials, password, 
				p_salt=users_salt, iv=users_iv))
			return True
		
	except Exception as e:
		print e
	
	return False

def encrypt(plaintext, password, iv=None, p_salt=None):
	if p_salt is not None:
		password = password + p_salt
		
	if iv is None:
		iv = Random.new().read(AES.block_size)
	else:
		iv = iv.decode('hex')
			
	aes = AES.new(
		hashlib.md5(password).hexdigest(), 
		AES.MODE_CBC,
		iv
	)
	
	ciphertext = {
		'iv' : iv.encode('hex'),
		'data' : aes.encrypt(pad(json.dumps(plaintext))).encode('hex')
	}
	
	return base64.b64encode(json.dumps(ciphertext))

def pad(plaintext):
	pad = len(plaintext) % AES.block_size
	
	if pad != 0:
		pad_from = len(plaintext) - pad
		pad_size = (pad_from + AES.block_size) - len(plaintext)
		plaintext = "".join(["*" for x in xrange(pad_size)]) + plaintext
	
	return plaintext

def unpad(plaintext):
	return plaintext[plaintext.index("{"):]
	
def decrypt(ciphertext, password, iv=None, p_salt=None):
	try:
		ct_json = json.loads(base64.b64decode(ciphertext))
		print ct_json
		
		ciphertext = ct_json['data'].decode('hex')

		if p_salt is not None:
			password = password + p_salt
		if iv is None:
			iv = ct_json['iv'].decode('hex')
		else:
			private_iv.decode('hex')

		aes = AES.new(
			hashlib.md5(password).hexdigest(),
			AES.MODE_CBC,
			iv
		)
		
		cookie_data = json.loads(unpad(aes.decrypt(ciphertext)))
		if cookie_data['username']:
			return cookie_data
	except KeyError as e:
		print e
	except ValueError as e:
		print e
		
	return None	
		
		