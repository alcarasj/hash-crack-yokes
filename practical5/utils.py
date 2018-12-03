import base64
import hashlib
from Crypto.Cipher import AES
from Crypto import Random

# This was all copied/taken from the provided assignment description. 
unpad = lambda s: s[:-ord(s[len(s) - 1:])]

def decrypt(enc, password):
	enc = base64.b64decode(enc)
	iv = enc[:16]
	cipher = AES.new(password, AES.MODE_CBC, iv)
	return unpad(cipher.decrypt(enc[16:]))

def pxor(pwd,share):
	words=share.split("-")
	hexshare=words[1]
	slen=len(hexshare)
	hashpwd=hashlib.sha256(pwd).hexdigest()
	hlen=len(hashpwd)
	outlen=0
	if slen<hlen:
		outlen=slen
		hashpwd=hashpwd[0:outlen]
	elif slen>hlen:
		outlen=slen
		hashpwd=hashpwd.zfill(outlen)
	else:
		outlen=hlen
	xorvalue=int(hexshare, 16) ^ int(hashpwd, 16) # convert to integers and xor 
	paddedresult='{:x}'.format(xorvalue)          # convert back to hex
	paddedresult=paddedresult.zfill(outlen)       # pad left
	result=words[0]+"-"+paddedresult              # put index back
	return result
