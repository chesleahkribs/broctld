import brctld


def spawn_bro():
	print "This should tell supervisor process to span bro process"

def start_supervisor():
	print "Start supervisor process"

def update():
	print "end main process"

def print_help_menu():
	print "quit\t\t-exit shell"
	print "exit\t\t-exit shell"
	print "start\t\t-start supervisor process"
	print "spawn\t\t-create new bro process"



if __name__ == "__main__":
	prompt =  "[BroControl] "

	print '\nWelcome to BroControl 1.4\n\nType "help" for help.\n\n'

	brctld.start_main();

	while True:
		n = raw_input(prompt)
		input = n.strip()

		if input == "exit":
			print "GOODBYE"
			break
		elif input == "help":
			print_help_menu()
		elif input == "update":
			update()
		elif input == "start":
			start_supervisor()
		elif input == "spawn":
			spawn_bro()
		else:
			print "Invalid Command"
