#!/usr/bin/env python3


# a sketch that will run a main thread and another one responsible to 
# read some GPIO values.

import threading, readchar, time, sys
import RPi.GPIO as GPIO

gpios = []

sharedVar = False

def checkInput():
	global sharedVar
	while True:
		print("Reading a char:")
		c = readchar.readchar()
		print( c )
		if c == ' ':
			sharedVar = True
			# exit thread execution
			return


def main():
	myThread = threading.Thread( target=checkInput )
	myThread.start()
	while True:
		if sharedVar:
			print("Trying to quit")
			quit()
		else:
			print( "main thread" )
			time.sleep(1)
	
	
if __name__ == "__main__":
	sys.exit( main() )
