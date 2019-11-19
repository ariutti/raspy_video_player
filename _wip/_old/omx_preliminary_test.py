#!/usr/bin/env python3

# a sketch to test Omxplayer used from inside
# a python script

#Import the required modules
import smbus, time, shlex, glob, random, sys
from subprocess import Popen, PIPE

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

	# split the command and use
	# the 'glob' module to expand the * wildchar
	#cmd = 'omxplayer --loop --no-osd --win "0 0 640 480" /home/pi/Videos/Aboca*'
	cmd = 'omxplayer --display 0 --loop --no-osd --win "0 0 320 200" /home/pi/Videos/Aboca*'
	args = shlex.split( cmd )
	args = args[:-1] + glob.glob( args[-1] )

	# Wait the system to boot up correctly
	#time.sleep(10)
	
	# Open omxplayer
	try:
		print( " load the video " )
		process = Popen( args, stdin=PIPE, stdout=PIPE )
		print("This is the omxplayer process id: ",  process.pid )
		print("go to start callbak")
		process.stdin.write(b'i')
		process.stdin.flush()
	except:
		print("something went wrong")
		quit()
		
	# Main loop
	while True:
		# check is someone plugged in a mouse or a keyboard
		if( areThereNewInputsDevices() ):
			# new input devices have been found
 			# script must be stopped in order
			# to let space for the user to work
			# with the Pi

			# quit omxplayer
			process.stdin.write(b'q')
			process.stdin.flush()
			process.stdin.close()

			# exit the python script
			quit()
		else:
			time.sleep(0.25)
			
if __name__ == '__main__':
	sys.exit( main() )
	

#End of the script
