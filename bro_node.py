#!/usr/bin/python

import socket
import threading
import subprocess
import sys
import os

config = open("broctld.config", "r")
conn = config.readlines()
host = conn[0]
port = int(conn[1])

def run_command(command):
	output = ''
	command = command.rstrip()
        #command = command + "; exit 0"
	output = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	for line in iter(output.stdout.readline, ''):
		print line
		sys.stdout.flush()

def quit_connection():
	node.close()
	os._exit(1)

print "Running Bro process..."
while 1:

	node = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	while 1:

		try:

			node.connect((host, port))
			break;
		except:
			pass
		
	while True:

		try:
			cmd = ""
			cmd=node.recv(1024)

			if (cmd == "quit" or cmd == "exit" or cmd == "close"):
				quit_connection()	
			else:			
				node.send("#")
				run_command(cmd)	
		except:
			node.close()
			break
