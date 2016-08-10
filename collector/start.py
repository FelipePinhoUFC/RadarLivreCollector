from threading import Thread, Event
from uploader import start as start_upload
from adsb import start as start_capture
from database import init as init_capture_resources

import os
import sys
import time
import report
import database

threadCapture = None
threadUploader= None
stopEvent = Event()

def stop():
	report.log("Stopping...")
	global stopEvent
	stopEvent.set()

def start():

	print "Starting collector"
	try:

		init_capture_resources()
		
		global threadCapture
		global threadUploader
		
		
		threadCapture = Thread(target = start_capture, args = (0, stopEvent))
		threadCapture.daemon = True
		threadCapture.start()

		threadUploader = Thread(target = start_upload, args = (1, stopEvent))
		threadUploader.daemon = True
		threadUploader.start()

		# threadCapture.join()
		# threadUploader.join()

		while True:
			time.sleep(1)

	except (KeyboardInterrupt, SystemExit):
		stop()
		sys.exit()
		
