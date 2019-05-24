#!/usr/bin/env python3

"""
# TEST DI INPUT CHAR
* https://stackoverflow.com/questions/510357/python-read-a-single-character-from-the-user
"""

"""
# EXAMPLE 1 - chiamata bloccante (aspetta un invio)
print('Enter your name:')
x = input()
print('Hello, ' + x)
"""

"""
# EXAMPLE 2 (va premuto invio dopo l'inserimento)
import sys
str = ""
while True:
    c = sys.stdin.read(1) # reads one byte at a time, similar to getchar()
    print( c )
    if c == ' ':
        break
    str += c
print(str)
"""

# a sketch that will run a main thread and another one responsible to 
# get new char fron the keyboard. If you press SPACEBAR, return will 
# retunr back to the main thread which will exit the program.

import threading, readchar, time, sys

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
