import os
from django.conf import settings
import tempfile
import subprocess
import shlex
import base64
class KKBSign(object):
	"""docstring for KBBSign"""
	def check(self,rawsign,data):
		tempSignature = tempfile.NamedTemporaryFile(mode="wb",delete=False)
		tempData = tempfile.NamedTemporaryFile(mode="wb",delete=False)
		tempPubKey = tempfile.NamedTemporaryFile(mode="wb",delete=False)
		rawsign = base64.b64decode(rawsign)[::-1]
		try:
			tempSignature.write(bytes(rawsign,'UTF-8'))
		except Exception as e:
			tempSignature.write(rawsign)
		tempSignature.seek(0)
		
		try:
			tempData.write(bytes(data,'UTF-8'))
		except Exception as e:
			tempData.write(data)
		tempData.seek(0)

		cmd = "".join(["openssl x509 -pubkey -noout -in ",settings.PUBLIC_KEY_FN])
		pubkey = subprocess.Popen(shlex.split(cmd),shell=False,stdin=subprocess.PIPE,stdout=subprocess.PIPE).communicate()[0]
		try:
			tempPubKey.write(bytes(pubkey,'UTF-8'))
		except Exception as e:
			tempPubKey.write(pubkey)
		
		tempPubKey.seek(0)

		cmd = "".join(["openssl dgst -sha1 -verify ", tempPubKey.name," -signature ",tempSignature.name," ",tempData.name])
		result = subprocess.Popen(shlex.split(cmd),shell=False,stdin=subprocess.PIPE,stdout=subprocess.PIPE).communicate()[0]
		
		tempPubKey.close()
		tempData.close()
		tempSignature.close()
		os.unlink(tempPubKey.name)
		os.unlink(tempData.name)
		os.unlink(tempSignature.name)
		return result.decode('utf-8')

	def sign64(self,text):		
		tempData = tempfile.NamedTemporaryFile(delete=False)
		try:
			tempData.write(bytes(text,'UTF-8'))
		except Exception as e:
			tempData.write(text)
		tempData.seek(0)

		tempSignature = tempfile.NamedTemporaryFile(mode="rb",delete=False)
		cmd = "".join(["openssl dgst -sha1 -sign ",settings.PRIVATE_KEY_FN," -passin ","".join(['pass:',settings.PRIVATE_KEY_PASS])," -out ",tempSignature.name," ",tempData.name ])
		p = subprocess.Popen(shlex.split(cmd),shell=False,stdin=subprocess.PIPE)
		p.communicate()
		signature = tempSignature.read()[::-1]
		tempData.close()
		tempSignature.close()
		os.unlink(tempData.name)
		os.unlink(tempSignature.name)
		return base64.b64encode(signature)
