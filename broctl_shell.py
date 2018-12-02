#!/usr/bin/python

import socket
import threading
import sys
import os
import time

print '\nWelcome to BroControl 1.4\n\nType "help" for help.\n\n'
a = "accept"
config = open("broctld.config", "r")	
conn = config.readlines()
ip_addr = conn[0]
port = int(conn[1])

supervisor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
supervisor.settimeout(5)
supervisor.bind((ip_addr, port))
supervisor.listen(10)

nodeSockets = []
nodeAddress = []

def get_previous_connections():

	print "Searching for previously connected nodes..."
	for item in nodeSockets:
		item.close()

	del nodeSockets[:]
	del nodeAddress[:]

	while 1:

		try:
			node,addr =  supervisor.accept()
			node.setblocking(1)
			nodeSockets.append(node)
			nodeAddress.append(addr)
		except:

			break
def get_new_connections():
	while 1:

		try:
			node,addr =  supervisor.accept()
			node.setblocking(1)
			nodeSockets.append(node)
			nodeAddress.append(addr)
		except:

			break


def close_socket():

	nodeSockets[cur_node].send("close")
	nodeSockets[cur_node].close()

def print_help_menu():
	print "show \t\t\t\t display all connected nodes"
	print "quit \t\t\t\t exit program"
	print "update \t\t\t\t close main function"	
	print "connect <node> \t\t\t\t interact with <node>"

	
while 1:
 
 	if a == "accept":
 		get_previous_connections()
 		a = "dont!"

	input = raw_input("\n[BroControl] ")

	if(input == "accept"):
		get_new_connections()
	elif (input == "show"):
		print "------------------\n\tNodes:\n------------------"
		for item in nodeAddress:
			print "%d - %s:%s" % (nodeAddress.index(item) + 1, str(item[0]), str(item[1]))
		print "\n"

	elif (input == "exit"):
		for item in nodeSockets:
			item.send("quit")
			item.close()
		os._exit(0)	
		#os._exit(1)

	elif (input == "update"):
			os._exit(0)

	elif(input == "help"):
		print_help_menu()		

	elif ("connect" in input):
		cur_node = int(input.replace("connect", "")) -1
		if  ((cur_node < len(nodeAddress)) and (cur_node >= 0)):

			node_prompt = "\n[BroControl] <node " + str(cur_node + 1)+ "> "
			while True:
		
				try:
					command = raw_input(node_prompt)

					if command == "exit":
						nodeSockets[cur_node].send(command)
						nodeSockets[cur_node].close()
						os._exit(1)
					
					elif command == "close":
							
						close_socket()
						break;

					elif ("cd " in command):
						
						nodeSockets[cur_node].send(command)
						msg=nodeSockets[cur_node].recv(4096)
						path = msg + ">"
						print "Changed dir to %s" % path
					
					elif command == "back":
						
						break;

					elif command == "run":	
						c = "python bro.py"
						nodeSockets[cur_node].send(c)
						# if recvd == # break loop and ask next command
						try :
							recvd = nodeSockets[cur_node].recv(4096)
							while "#" not in recvd:
								recvd = recvd.rstrip('\n')
								print recvd
								recvd = nodeSockets[cur_node].recv(4096)
						except KeyboardInterrupt:
							pass	
					
				except Exception, e:
					pass