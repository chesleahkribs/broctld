#!/usr/bin/python

from multiprocessing.connection import Client
from multiprocessing.connection import deliver_challenge
from multiprocessing import Process
import sys
import os
import subprocess
import time
import traceback
import datetime

#Random Commands
	#print subprocess.check_output("ls", shell=True)


def spawn_bro(address, port):
	command = "gnome-terminal -- python bro_test.py {} {}".format(address, port)
	os.system(command)

def get_nodes(node_file, nodes):

	#nodes structure: [[addr, port, TF:connected],...]
	#read in list of nodes
	config = open(node_file, "r")
	for line in config:
		a, p = line.replace('\n','').split(':')
		nodes.append([a, p, False])
	config.close()

def check_nodes(nodes, inactive_nodes, connections):
	for con, node in zip(connections, nodes):
		try:
			deliver_challenge(con, authkey="hi")
			print "{} is connected".format(node)
		except EOFError:
			print "{} is not connected".format(node)
			node[2] = False
			con.close()
			connections.remove(con)
			nodes.remove(node)
			inactive_nodes.append(node)

def connect_node(node):
	try:

		#connect
		address = (node[0], int(node[1]))
		connect = Client(address, authkey="hi")
		connect.send('Hello from supervisor process')

		#check connection
		try:
			deliver_challenge(connect, authkey="hi")
			print "Node {} connected".format(node)
			node[2] = True
			return connect

		except EOFError:
			traceback.print_exc()
			print "Could not connect to node {} {}".format(node[0], node[1])
			node[2] = False
			con.close()

	except:
		traceback.print_exc()
		print "Could not connect to node {} {}".format(node[0], node[1])
		node[2] = False


def supervisor():
	nodes = []
	inactive_nodes = []
	connections = []
	#read in list of nodes
	get_nodes("nodes.config", nodes)
	
	#spawn and connect to bro nodes
	i = 0
	for node in nodes:
		i = i + 1
		print "attempting to spawn node: {}".format(i)
		spawn_bro(str(node[0]), int(node[1]))
		time.sleep(1)
		con = connect_node(node)
		if not node[2]:
			inactive_nodes.append(node)
			print "Node {} is inactive".format(node)
			nodes.remove(node)
		else:
			connections.append(con)

	time.sleep(2)
	
	while True:
		print "{}: checking active nodes".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
		check_nodes(nodes, inactive_nodes, connections)

		if(len(inactive_nodes) > 0):
			print "Trying to connect all inactive nodes"
			for node in inactive_nodes:
				print node
				spawn_bro(str(node[0]), int(node[1]))
				con = connect_node(node)
				if(node[2]):
					inactive_nodes.remove(node)
					nodes.append(node)
					connections.append(con)
		time.sleep(10)

	time.sleep(2)
	for con in connections:
		con.close()	

	time.sleep(10)

#for f, b in zip(foo, bar):
#    print(f, b)

if __name__ == "__main__":
	p1 = Process(target=supervisor)
	p1.start()