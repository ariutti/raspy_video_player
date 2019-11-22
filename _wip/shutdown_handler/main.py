#!/usr/bin/env python3

import sys, random, time
import threading, socket, os

# 2018-12-13: this method is in charge to shutdown the pi when it gets
# a "shutdown" message string via socket. Before doing this the method
# is also responsible to shutdown everything is currently running
def shutdownHandler():
	print("Shutdown handler: started")
	conn = None
	addr = None
	mysock = None
	
	try:
		mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	except socket.error:
		print("Failed to create socket")
		sys.exit()

	try:
		mysock.bind( ("", 1234) )
	except socket.error:
		print("Failed to bind")
		mysock.close()
		sys.exit()

	# backlog (quante richieste in attesa sono consentite)
	mysock.listen(1)

	# Live server
	while True:
		conn, addr = mysock.accept()
		data = conn.recv(1000)
		if not data:
			break
		if data == b"shutdown":
			print("quitting")
			break
		else:
			print("what?")
	
	# if we are here it means someone asked the pi to shutdown
	# so we cal the shell script in charge of doing this.
	# Inside the script there's an instruction to wait 10 secs
	# before shutting down. in the meantime we can close the OSC server,
	# socket connections and exit the python program!
	print("calling external script")
	try:
		os.system('./shutdown_script.sh &')
	except:
		print("I wasn't able to call the shutdown script")

	print("trying to close everything")
	
	# close here the thing to be closed
		
	conn.close()
	mysock.close()
	sys.exit(0)


if __name__ == "__main__":
	#global printers, landscapes, OSCSERVER_IP
	print("MAIN program start\n")
	
	print("waiting 10 secs")
	#time.sleep(10)
	
	"""
	# get my IP address
	import os
	f = os.popen('ifconfig eth0 | grep inet')
	s = f.read()
	print( s )
	OSCSERVER_IP = s.split()[1]
	"""
	
	# start the shutdown handler function.
	# It will take care of opening and listening on a socket
	# for a "shutdown message".
	shutdownHandler()

