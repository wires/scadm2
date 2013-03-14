import os
import json, pygments
import soundcloud

import requests

from progressbar import ProgressBar, AnimatedMarker

class Abort(Exception):
	def msg(self):
		return self.args[0]
	pass

def authload(authfile = 'auth.py'):
	authmsg = """ERROR: place auth data in %s, like:
	
	# make sure to chmod 600 this file
	username = 'foobar'
	password = 'b@n@n@'
	CLIENT_ID     = 'c475209b276ea4725abe92453088150c'
	CLIENT_SECRET = '8096dc915eadc415ae41b9d5d514295d'
	"""

	# make sure file exists
	if not os.path.isfile(authfile):
		raise Abort(authmsg % authfile)

	# make sure it is chmod 600
	if not oct(os.stat(authfile).st_mode).endswith('600'):
		raise Abort("make sure %s is chmod 600 (rw-------)" % authfile)

	import auth
	return auth

class DummyProgressBar:
	def __call__(_,v):
		return v
	def finish(_):
		pass

class SC:
	def __init__(s,auth,pbar=True):
		# yes or no progress bar?
		s.pbar = pbar
		s.client = soundcloud.Client(
			client_id=auth.CLIENT_ID,
			client_secret=auth.CLIENT_SECRET,
			username=auth.username,
			password=auth.password
		)
	
		if not s.client:
			Abort("failed to login to soundcloud")

	def _pbar(self, s):
		# return dummy (no progress bar)
		if not self.pbar:
			return DummyProgressBar()

		# or construct real progressbar
		w = [s, AnimatedMarker(markers="|/-\|")]
		return ProgressBar(widgets=w)

	def r(self, s, **kwargs):
		obj = self.client.get(s, **kwargs)

		# single resource
		if type(obj) == soundcloud.resource.Resource:
			return obj.fields()

		# list of resources
		return [r.fields() for r in obj]

	def test(self):
		pbar = self._pbar('sleeping: ')
		import time
		for i in pbar(range(10)):
			time.sleep(0.1)
	
	# page over list of resources
	# TODO use itertools!! do this lazy
	def rs(self, s, maximum=10**5, k=32):
		def log(wut):
			import sys
			sys.stdout.write('\r%s' % wut)
			sys.stdout.flush()

		rs = []
		for i in range(0,maximum,k):
			rs += self.r(s,limit=k,offset=i)
			log("loading %s: %d" % (s, len(rs)))
			if len(rs) % k:
				break
		log("loaded %d items from %s\n" % (len(rs),s))
		return rs

	def stream(s, track_id):
		stream = s.r('/tracks/%d/stream' % track_id, allow_redirects=False)
		r = requests.get(stream['location'], stream=True)
		return r.raw
