#!/usr/bin/env python3

## AN EXPERIMENT IN USING OMXPLAYER TO PLAY A VIDEO MEDIA FILE

"""
## TODO (BUG/ISSUES/IMPROVEMENTS)
* errore DBUS (sembra risolto
	https://github.com/popcornmix/omxplayer/issues/46
* omx fullscree
	https://github.com/huceke/omxplayer/issues/44
"""


#Import the required modules
import smbus, time, shlex, glob, random, sys
from subprocess import Popen, PIPE


# global variable to be used
# for scanning input devices
#inputLen
#prevInputLen

'''
def retryLater():
	global TIME_MIN, TIME_MAX
	timeToWait = float( random.randint( TIME_MIN, TIME_MAX ) )
	#print( timeToWait )
	time.sleep( timeToWait / 1000.0 )


def teminate():
	command = "/usr/bin/sudo /sbin/shutdown now"
	#import subprocess
	#process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
	#output = process.communicate()[0]
	process = Popen(command.split(), stdout=PIPE)
	print output
'''


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
		print("Hey! A new input device has been plugged")
		return True
	else:
		print( "input devices are now equals or less than before" )
		print( str(inputLen) + " " + str(prevInputLen) )
		prevInputLen = inputLen
		return False


if __name__ == '__main__':
	#rint( "main" )
	global inputLen, prevInputLen

	inputLen = getInputDevices()
	prevInputLen = inputLen

	# split the command and use
	# the 'glob' module to expand the * wildchar
	#cmd = 'omxplayer --loop --no-osd --win "0 0 640 480" /home/pi/Videos/Aboca*'
	cmd = 'omxplayer --loop --no-osd --win "0 0 640 480" /home/pi/Videos/Aboca*'
	args = shlex.split( cmd )
	args = args[:-1] + glob.glob( args[-1] )

	# Wait the system to boot up correctly
	#time.sleep(10)

	# Open the i2c bus 0 ( /dev/i2c-0 )
	#bus = smbus.SMBus( 0 )

	
	# Open omxplayer
	try:
		print( " load the video " )
		process = Popen( args, stdin=PIPE, stdout=PIPE )
		print("This is the omxplayer process id: ",  process.pid )
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
		"""
		else:
			process.stdin.write( b'i' )
			process.stdin.flush()
			time.sleep(1)
		"""
			

		
		#try:
		#	data = bus.read_byte( ARDUINO_ADDRESS )
		#except:
		#	# If the i2c bus is unavailable/busy at the moment,
		#	# wait before trying to use it again.
		#	#print( "exception intercepted!" )
		#	timeToWait = float( random.randint( TIME_MIN, TIME_MAX ) )
		#	#print( timeToWait )
		#	time.sleep( timeToWait / 1000.0 )
		#	continue

		# If we are here it means we got some data from the bus.
		# Time to use it.

		# Uncomment lines below to see a debug print
		#print( "curr: " + str(data) + "; prev: " + str(prevData) + ";" )

		#if( data >= 0 and data <10 ):
		#	if( data != prevData ):
		#		process.stdin.write( str( data ) )
		#		process.stdin.flush()
		#		prevData = data

		"""
		if( data == ord('i') ):
			if( data != prevData ):
				#print( "prev chapter: " )
				#print( "curr: " + str(data) + "; prev: " + str(prevData) + ";" )
				process.stdin.write(b'i')
				process.stdin.flush()
				prevData = data
				time.sleep(1)
				continue

		elif( data == ord('a') ):
			if( data != prevData ):
				#print( "curr: " + str(data) + "; prev: " + str(prevData) + ";" )
				# This is a jolly case:
				# we do nothing but update prev chapter
				prevData = data
				time.sleep(1)
				continue

		elif( data == ord('q') ):
			print( "Quitting OMX player!" )

			# quit omxplayer
			process.stdin.write(b'q')
			process.stdin.flush()
			process.stdin.close()

			# shutdown the Raspberry
			#print( " ready to shutdown ")
			command = "/usr/bin/sudo /sbin/shutdown now"
			proc = Popen(command.split(), stdout=PIPE)
			output = proc.communicate()[0]

			# exit the python script
			# (Will we ever touch this line?!)
			quit()

		# This portion of code is reached only when the raspi,
		# after having found data on the I2C bus:
		# * is not reading anything new on the i2c bus;
		# * the data on the i2c is not valid.

		timeToWait = float( random.randint( TIME_MIN, TIME_MAX ) )
		#print( timeToWait )
		time.sleep( timeToWait / 1000.0 )
		"""
		time.sleep(1)


#End of the script
