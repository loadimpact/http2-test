#!/usr/bin/python
import shlex
import subprocess
import re
import time
import os 
import raven

SENTRY_DSN = "https://92c022942c894d66bcee424d1d2f23e7:e1dd1542019549cbba94ac5cc164d274@app.getsentry.com/39820"


sentry_client = raven.Client(
	dsn=SENTRY_DSN,
	site="StationB/onstartup.py")


#google-chrome
def tool(cmdstr):
    pieces = shlex.split(cmdstr)
    o = subprocess.check_output(pieces)
    return o 

def run(cmdstr):
    pieces = shlex.split(cmdstr)
    p = subprocess.Popen(pieces)
    return p

chrome_process = run("google-chrome --disable-gpu")

while True:
	time.sleep(4.0)
	s = tool("xwininfo -tree -root")
	mo = re.search(r"\s+(0x[a-f0-9]+) \".*?Google Chrome\"", s)
	if mo is None:
		sentry_client.captureMessage("Couldn't find Google chrome windows")
		if chrome_process.returncode is not None:
			sentry_client.captureMessage("Chrome exited with code {0}".format(chrome_process.returncode))
			exit(1) 
	else:
		break

winid = mo.group(1)
print("Win id:", winid)
tool("xdotool click --window {0} 1".format(winid))
time.sleep(0.5)
tool("xdotool key --window {0} \"ctrl+shift+i\"".format(winid))
time.sleep(0.5)
# Get chrome as full-screen, so to make taking screenshots easier.
tool("xdotool key --window {0} \"F11\"".format(winid))
chrome_process.wait()
