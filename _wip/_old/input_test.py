#!/usr/bin/env python3

# a sketch to check the number of input
# peripherals connected to the py

#Import the required modules
import smbus, time, shlex, glob, random, sys
from subprocess import Popen, PIPE

# global variable to be used
# for scanning input devices
inputLen = None
prevInputLen = None
process = None
	

def getInputDevices():
	cmd  = 'ls /dev/input'
	args = shlex.split( cmd )
	proc = Popen( args, stdout=PIPE )
	output = proc.communicate()[0]
	return len( output.split() )


def areThereNewInputsDevices():
	global inputLen, prevInputLen
	inputLen = getInputDevices()

	# Quit the script only when you plug a new input device.
	# Do nothing but update the 'prevInputLen' when removing it.
	if( inputLen > prevInputLen ):
		#print("Hey! A new input device has been plugged")
		return True
	else:
		#print( "input devices are now equals or less than before" )
		#print( str(inputLen) + " " + str(prevInputLen) )
		prevInputLen = inputLen
		return False


def main():
	#print( "main" )
	global inputLen, prevInputLen, process

	inputLen = getInputDevices()
	prevInputLen = inputLen	

	# Main loop
	while True:
		# check is someone plugged in a mouse or a keyboard
		if( areThereNewInputsDevices() ):
			# exit the python script
			quit()
		else:
			#print("running")
			time.sleep(1)

if __name__ == '__main__':
	sys.exit( main() )
	
#End of the script
