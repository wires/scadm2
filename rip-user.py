import sys, os, json
from fn import _
from pp import pp

import sc

# login or report error
try:

	# load authentication data
	auth = sc.authload()

	# connect client
	client = sc.SC(auth)

except sc.Abort, a:
	print a.msg()
	sys.exit(1)

def ppr(s):
	"""pretty result of executing the soundcloud API request s"""
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
	comments = fn('comments.json')

        c = client.r('/tracks/%d/comments' % i)
	print("%s has %d comments" % (audio, len(c)))
	with open(comments, 'w+') as f:
		json.dump(c, f)

	if not os.path.exists(audio):
		print "downloading %s" % audio
		with open(meta, 'w+') as f:
			json.dump(track, f)

		with open(audio, 'wb+') as f:
			f.write(client.stream(i).read())
	else:
		print "file already exists, skipping %s" % audio


# program starts here:

from requests.exceptions import HTTPError

u = sys.argv[1]
user = client.r('/users/' + u)
pp(select(user, ["id", "track_count"]))

comments = client.r('/users/%s/comments' % u)
print("%s has %d comments" % (u, len(comments)))
with open('users/%s.comments.json' % u, 'w+') as f:
	json.dump(comments, f)

t = "artwork_url,bpm,comment_count,genre,id,playback_count,tag_list,title"
t = t.split(',')
tracks = client.rs('/users/%d/tracks' % user['id'])
for track in tracks:
	try:
		pp(select(track, t))
		download("users/%s/" % u, track)
	except HTTPError,e:
		print e
		print "skipping track %s" % track['title']
		continue
