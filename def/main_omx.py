#!/usr/bin/env python3

# OMX PLAYER and GPIO integration
# Thank to Phasor1 for precious support

# CHANGE VIDEO FILE NAME HERE **************************************************

#PATH_TO_VIDEO_FILE = "/home/pi/Videos/alvanoto.mp4"
#PATH_TO_VIDEO_FILE = "/home/pi/Videos/Aboca/ABOCA_NASCITA_60SEC_ITA_innovazione per la salute.mp4"
#PATH_TO_VIDEO_FILE = "/home/pi/Videos/Aboca/Kennedy_HD.mp4"
#PATH_TO_VIDEO_FILE = "/home/pi/Videos/Aboca/ABOCA_InfiniteZoom_ITALIA_ABOCAINNOVAZIONE_2.mov"
PATH_TO_VIDEO_FILE = "/home/pi/Videos/Aboca/Aboca_IST_ITA_subENG_set2018.mp4"

# DO NOT CHANGE ANYTHING BELOW *************************************************

#Import the required modules
import smbus, time, shlex, glob, random, sys, socket, os, threading
from subprocess import Popen, PIPE

# global variable to be used
# for scanning input devices
inputLen = None
prevInputLen = None
process = None

from omxplayer.player import OMXPlayer
videoPlayer = None
B_USE_VIDEO = True

# time in seconds to wait for the user to bring the speaker to his hear
# before start the video reproduction
COURTESY_TIME = 1
AUDIO_MAX_VOLUME = 1.0
AUDIO_MIN_VOLUME = 0.0


from buttonManager import ButtonManager

# A callback to be passed to the button manager.
# It will be called when at least one of the two audio receiver
# has been lifter
def goToStart_CB():
	global videoPlayer
	print("** go to start callback **")
	print( "    start video from position 0.0")
	if B_USE_VIDEO:
		videoPlayer.pause()
		time.sleep( COURTESY_TIME )
		videoPlayer.set_position(0.0)
		videoPlayer.set_volume( AUDIO_MAX_VOLUME )
		# the video is in pause so start playing it
		videoPlayer.play()


# A callback to be passed to the button manager.
# It will be called when both the audio receivers
# will be hanged up
def muteAudio_CB():
	global videoPlayer
	print("** mute audio callback **")
	print( "    mute audio ")
	if B_USE_VIDEO:
		videoPlayer.set_volume( AUDIO_MIN_VOLUME )
		#videoPlayer.pause()


# CHECK INPUT DEVICES STUFF ****************************************************
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
		#print( "input devices are now {} equals or less than before {}".format(inputLen, prevInputLen) )
		prevInputLen = inputLen
		return False


"""
#20200714 - not used anymore
checkPositionThread = None
position = None
def checkLength():
	global videoPlayer, position
	while 1:
		if B_USE_VIDEO:
			position = videoPlayer.get_position() # 0.0 - 1.0 position
			#print( "player position: {}".format( position ) )
		time.sleep(0.1)
"""

# SHUTDOWN HANDLER STUFF *******************************************************

shutdownHandlerThread = None
# This method is in charge to shutdown the pi when it gets
# a "shutdown" message string via socket. Before doing this the method
# is also responsible to shutdown everything is currently running
def shutdownHandler():
	print("SHUTDOWN HANDLER: started")
	conn = None
	addr = None
	mysock = None

	try:
		mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	except socket.error:
		print("SHUTDOWN HANDLER: Failed to create socket")
		sys.exit()

	try:
		mysock.bind( ("", 1234) )
	except socket.error:
		print("SHUTDOWN HANDLER: Failed to bind")
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
			print("SHUTDOWN HANDLER: quitting")
			break
		else:
			print("SHUTDOWN HANDLER: what?")

	# if we are here it means someone asked the pi to shutdown
	# so we cal the shell script in charge of doing this.
	# Inside the script there's an instruction to wait 10 secs
	# before shutting down. in the meantime we can close the OSC server,
	# socket connections and exit the python program!
	print("SHUTDOWN HANDLER: calling external script")
	try:
		os.system('./shutdown_script.sh &')
	except:
		print("SHUTDOWN HANDLER: I wasn't able to call the shutdown script")

	print("SHUTDOWN HANDLER: trying to close everything")

	# close here the thing to be closed

	conn.close()
	mysock.close()
	sys.exit(0)


# MAIN START HERE **************************************************************

def main():
	#print( "main" )
	global inputLen, prevInputLen, videoPlayer

	# Open video player
	try:
		print( "MAIN: load the video " )
		videoPlayer = OMXPlayer(PATH_TO_VIDEO_FILE, args=['--no-osd', '--adev', 'local'])
		#videoPlayer.set_volume( AUDIO_MIN_VOLUME )

		#2020-13-07 - we are not using VLC anymore :(
		# ~ videoPlayer = vlc.MediaPlayer( PATH_TO_VIDEO_FILE )
		#process = Popen( args, stdin=PIPE, stdout=PIPE )
		#print("This is the omxplayer process id: ",  process.pid )

	except Exception as exc:
		print("MAIN: something went wrong in creating the OMX video player {}".format(exc) )
		quit()

	#2020-13-07 - we are not a separate thread anymore to check for the actual playhead position
	#checkPositionThread = threading.Thread(target=checkLength)
	#checkPositionThread.start()

	print( "MAIN: video length {}".format(videoPlayer.duration() ) )

	if B_USE_VIDEO:
		videoPlayer.set_volume(AUDIO_MIN_VOLUME)
		# 2020-07-13 - no need to use fullscreen anymore
		# ~ videoPlayer.toggle_fullscreen() # use it to go fullscreen
		videoPlayer.play()


	# initialize Button manager
	buttonManager = ButtonManager(goToStart_CB, muteAudio_CB, polarity=False)

	# get the current number of connected input devices
	inputLen = getInputDevices()
	prevInputLen = inputLen

	# start the shutdown handler function.
	# It will take care of opening and listening on a socket
	# for a "shutdown message" in order to kill the python process
	# and shutdown the RaspberryPi
	shutdownHandlerThread = threading.Thread(target=shutdownHandler)
	shutdownHandlerThread.start()


	# Main loop
	while True:
		# check if someone plugged in a mouse or a keyboard
		if( areThereNewInputsDevices() ):
			# if a new input device has been found, tthis very script
			# must be stopped in order to let space for the user to work
			# with the Pi, so...

			# quit video player
			videoPlayer.stop() # will exit current vlc window (desktop will be visible)

			# TODO: kill all alive thread
			# find a way to do this

			# exit the python script
			quit()
		else:
			buttonManager.update()
			#print("MAIN: position {}".format(position) )
			if B_USE_VIDEO:
				position = videoPlayer.position()
				if videoPlayer.duration() - position <= 1:
					videoPlayer.set_position( 0.0 )
			time.sleep(0.1)


if __name__ == '__main__':
	sys.exit( main() )

#End of the script
