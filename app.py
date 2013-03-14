import sys, os, json
from fn import _
from pp import pp

import sc

# login or report error
try:

	# load authentication data
	auth = sc.authload()

	# connect client
	client = sc.SC(auth, pbar=True)

except sc.Abort, a:
	print a.msg()
	sys.exit(1)

def ppr(s):
	pp(client.r(s))

def select(D,keys):
	return dict((k,v) for k,v in D.items() if k in set(keys))

def proj(D,path):
	c = D
	for p in path.split("."):
		c = c[p]
	return c

def download(target, track):
	user = track['user']['permalink']
	i = track['id']
	fn = lambda ext: "%s/%s-%d.%s" % (target, user, i, ext)
	audio = fn('mp3')
	meta = fn('meta.json')
	print "downloading %s" % audio
	with open(meta, 'w+') as f:
		json.dump(track, f)

	if not os.path.exists(audio):
		with open(audio, 'wb+') as f:
			f.write(client.stream(i).read())
	else:
		print "file already exists, skipping"


# program starts here:

group = client.r('/me/groups')[0]
pp(select(group,["name","id"]))

def pending(g):
	return client.rs('/groups/%d/pending_tracks' % g['id'],  maximum=300)

t = "artwork_url,bpm,comment_count,genre,id,playback_count,tag_list,title"
t = t.split(',')

for track in pending(group):
	pp(select(track,t))
	download("pending", track)

