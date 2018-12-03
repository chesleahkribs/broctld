#!/usr/bin/python

import multiprocessing
import socket
import sys
import os

def spawn_bro(address, port):
	pass

def get_nodes(node_file, nodes):

	#nodes structure: [[addr, port],...]
	#read in list of nodes
	config = open(node_file, "r")	
	for line in config:
		a, p = line.replace('\n','').split(':')
		nodes.append([a,p])
	config.close()

def check_nodes():
	pass



if __name__ == "__main__":
	nodes = []

	#read in list of nodes
	get_nodes("nodes.config", nodes)

	for node in nodes:
		print node
