
cat afex | xargs -n1 -I_ mkdir -p users/_
cat afex | xargs -n1 -I_ python rip-user.py _
