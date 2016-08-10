import os
import datetime
import inspect
from config import LOG_DIR

LOG_FILE = "all.log"
LOG_FILE_INFO = "info.log"
LOG_FILE_ERROR = "error.log"

def setupLogDir():

	if not os.path.exists(LOG_DIR):
		os.makedirs(LOG_DIR)

def setupLogFile():

	setupLogDir()
	logFilePath = os.path.join(LOG_DIR, LOG_FILE)
	logFile = open(logFilePath, 'a')
	return logFile


def setupLogFileInfo():

	setupLogDir()
	logFilePath = os.path.join(LOG_DIR, LOG_FILE_INFO)
	logFile = open(logFilePath, 'a')
	return logFile


def setupLogFileError():
	
	setupLogDir()
	logFilePath = os.path.join(LOG_DIR, LOG_FILE_ERROR)
	logFile = open(logFilePath, 'a')
	return logFile


def info(message):
	logi = setupLogFileInfo()
	logi.write(str(datetime.datetime.now()) + " - " + message + "\n")
	logi.close()
	log(message)


def error(message):
	loge = setupLogFileError()
	loge.write(str(datetime.datetime.now()) + " - " + message + "\n")
	loge.close()
	log(message)

def log(message):
	log = setupLogFile()
	log.write(str(datetime.datetime.now()) + " - " + message + "\n")
	log.close()

	print str(datetime.datetime.now()) + " - " + message

def getLog():
	setupLogDir()
	logFilePath = os.path.join(LOG_DIR, LOG_FILE)
	file = open(logFilePath, 'r')
	log = file.read()
	file.close()
	return log

def clear():
	setupLogDir()
	logFilePath = os.path.join(LOG_DIR, LOG_FILE)
	open(logFilePath, 'w').close()