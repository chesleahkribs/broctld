import multiprocessing
from paramiko.client import SSHClient
import psutil

client = SSHClient()
client.load_system_host_keys()

password = raw_input("enter your password")
client.connect('linprog@cs.fsu.edu', username='minter', password=password)
stdin, stdout, stderr = client.exec_command('python /home/grads/minter/cop5570/groupproject/test.py')