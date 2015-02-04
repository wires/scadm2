# About

Tool to pull down aphex stuff

File `afex` has a list of users, this creates folders for each user and
then downloads (save stream) the tracks + the comments

	cat afex | xargs -n1 -I_ mkdir -p users/_
	cat afex | xargs -n1 -I_ python rip-user.py _

### TODO

- artwork
- high quality downloads

# Features

- Download all pending tracks + metadata

# Quickstart

First we clone and then setup dependencies, usual python stuff,

	git clone https://github.com/0x01/scadm2.git
	cd scadm2

	virtualenv venv
	source venv/bin/activate
	pip install -r requirements.txt

Now, create a file called `auth.py` containing your soundcloud user name
and password. You also need a `CLIENT_ID` and `CLIENT_SECRET` obtainable
from the soundcloud developer page.

	# make sure to chmod 600 this file
	username = 'foobar'
	password = 'b@n@n@'
	CLIENT_ID     = 'c475209b276ea4725abe92453088150c'
	CLIENT_SECRET = '8096dc915eadc415ae41b9d5d514295d'

We now need a folder to store the pending files:

	mkdir pending/

Then just run the app,

	python app.py

All pending tracks are downloaded to `pending/username-trackid.mp3`,
including metadata into `.meta.json`.
