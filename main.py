#!/usr/bin/python

from multiprocessing import Process
import os
import time

def spawn_supervisor():
	command = "gnome-terminal -- python supervisor.py"
	os.system(command)

if __name__ == "__main__":
	print "Hello"
	spawn_supervisor()
	time.sleep(5)