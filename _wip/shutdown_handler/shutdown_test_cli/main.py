#!/usr/bin/env python3

import socket, sys, time, getopt

PORT = 1234
timetowait = 1


def usage():
	print("Usage: 'main.py -i <computer/raspberry ip>'")


if __name__ == "__main__":
	print("Main program start")
	ip = "192.168.1.42"
	
	# richeista di get generica (la più generica possibile)
	# asking for the content of the web page
	# (ADD: uso b per conbertire la stringa in byte così
	# da poterla inviare)
	#message = b"GET / HTTP/1.1\r\n\r\n"
	message = 'shutdown'
	
	
	# parse the arguments	
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hi:", ["help", "ip="])
	except getopt.GetoptError as err:
		#print help info and exit
		print(err)
		usage()
		sys.exit(2)
		
	if len(opts) < 1 or len(opts) > 1:
		print("too many/few arguments")
		usage()
		sys.exit(2)
	
	
	for o, a in opts:
		if o in ("-h", "--help"):
			usage()
			sys.exit(2)
		elif o in ("-i", "--ip"):
			ip = a
		else:
			usage()
			sys.exit(2)
	
	print("creating socket")
	try:
		# SOCK_STREAM means TCP (not UDP)
		mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	except socket.error:
		print("\tFailed to create socket")
		sys.exit()
		
	# must wait some time in order for VVVVV
	# to read and crunch the message
	time.sleep( timetowait )


	print("connecting")
	try:
		# serve conoscere anche la porta (80 è il traffico web)
		print("using {} as destination IP and {} as port".format(ip, PORT) )
		mysock.connect( (ip, PORT) )
	except socket.error:
		print("\tUnable to connect")
		sys.exit()
		
	# must wait some time in order for VVVVV
	# to read and crunch the message
	time.sleep( timetowait )

	try:
		# sendall cerca di inviare fino a che non ce la fa!
		print("sending")
		mysock.sendall( message.encode() )
	except socket.error:
		print("Failed to send data")
		sys.exit()

	'''
	m = mysock.recv(1024) # blocking
	print( m )
	'''
	print("closing socket")

	# must wait some time in order for VVVVV
	# to read and crunch the message
	time.sleep( timetowait )

	# è importante liberare la porta così altri processi
	# che ne abbiano bisogno la possono usare
	mysock.close()
	
	time.sleep( timetowait )


	# error handling
	# nei socket possono capitare una marea di errori.
	# la socket non può essere aperta
	# i dati non possono essere inviati

	# E' la classe più generica degli errori di socket
	# socket.error
	# E' il get address info error (ottenuto dal DNS lookup)
	# quando non trova l'indirizzo del server
	# gaierror
