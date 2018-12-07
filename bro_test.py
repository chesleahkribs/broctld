#!/usr/bin/python
import sys
import time
from multiprocessing.connection import Listener
from multiprocessing.connection import answer_challenge
from multiprocessing import Process
import traceback

def challenge():
	while(True):
		answer_challenge(supervisor_connection, authkey="hi")
		print "answered challenge"

if __name__ == '__main__':
	print "bro IP: {}, port: {}".format(sys.argv[1], sys.argv[2])

	address = (sys.argv[1], int(sys.argv[2]))
	print address
	listener = Listener(address, authkey="hi")	#listener(address, authkey='pw')
	#try:
	supervisor_connection = listener.accept()
	#except:
	#	print "Connection to supervisor failed"
	#	exit()

	print "Connected to supervisor"
	temp = supervisor_connection.recv()
	print temp
	answer_challenge(supervisor_connection, authkey="hi")

	#p = Process(target=challenge)
	#p.start()

	while True:
		answer_challenge(supervisor_connection, authkey="hi")
		print "answered challenge"

	while True:
		time.sleep(10)

	supervisor_connection.close()
	listener.close()