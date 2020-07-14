#!/usr/bin/env python3

# VLC PLAYER and GPIO integration

# 2019-11-19 - TODO
# 1. test with real file - DONE
# 2. test loop
# 3. add a functionality for pushbutton polarity inversion - DONE
# 4. ridimensiona finestra di rendering
# 5. aggiungi un sistema per tenere traccia della posizione relativa della playhead - DONE
# 6. improve thread managment
# 7. add a way to pause video when both buttons are not operated - DONE
# 8. test playlist mode
 
#Import the required modules
import smbus, time, shlex, glob, random, sys
from subprocess import Popen, PIPE

# see: https://git.videolan.org/?p=vlc/bindings/python.git;a=blob;f=generated/3.0/vlc.py;h=e3245a5116946a4b52cadf5642441daa97af022d;hb=HEAD 
# and: https://olivieraubert.net/vlc/python-ctypes/doc/vlc.MediaPlayer-class.html
# for reference

import vlc
videoPlayer = None
bUseVideo = True
#time in seconds to wait for the user to bring the speaker to his hear
# before start the video reproduction
courtesyTime = 1
audioMaxVolume = 70 # 0 - 100


#pathToVideoFile = "/home/pi/Videos/Aboca/Aboca_IST_ITA_subENG_set2018.mp4"
pathToVideoFile = "/home/pi/Videos/Aboca/Aboca_VideoCavaliere_subENG_60sec_giu2020.mp4"

# global variable to be used
# for scanning input devices
inputLen = None
prevInputLen = None
process = None

from buttonManager import ButtonManager
		
def goToStartCallBack():
	global videoPlayer
	print("** go to start callback **")
	if bUseVideo:
		videoPlayer.pause()
		time.sleep( courtesyTime )
		videoPlayer.set_position(0.0)
		videoPlayer.audio_set_volume( audioMaxVolume )
		# the video is in pause so start playing it
		videoPlayer.play()
	
def pauseVideoCallBack():
	global videoPlayer
	print("** pauseVideo callback **")
	if bUseVideo:
		videoPlayer.pause() 
		
def muteAudioCallBack():
	global videoPlayer
	print("** muteAudio callback **")
	if bUseVideo:
		videoPlayer.audio_set_volume( 0 )
	

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

import threading, socket, os
checkPositionThread = None
position = None
def checkLength():
	global videoPlayer, position
	while 1:
		if bUseVideo:
			position = videoPlayer.get_position() # 0.0 - 1.0 position
			#print( "player position: {}".format( position ) )
		time.sleep(0.1)
		

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

def main():
	#print( "main" )
	global inputLen, prevInputLen, videoPlayer, position

	# Wait the system to boot up correctly
	#time.sleep(10)
	
	# Open video player
	try:
		print( "MAIN: load the video " )
		videoPlayer = vlc.MediaPlayer( pathToVideoFile )
		#process = Popen( args, stdin=PIPE, stdout=PIPE )
		#print("This is the omxplayer process id: ",  process.pid )
	except Exception as exc:
		print("MAIN: something went wrong {}".format(exc) )
		quit()
	
	checkPositionThread = threading.Thread(target=checkLength)
	checkPositionThread.start()
	
	print( "MAIN: video length {}".format(videoPlayer.get_length() ) )
	
	if bUseVideo:
		videoPlayer.audio_set_volume( audioMaxVolume )
		videoPlayer.toggle_fullscreen() # use it to go fullscreen
		videoPlayer.play()
		
		#time.sleep(1)
		#videoPlayer.pause()
		#videoPlayer.video_set_scale(0.5)
	
	#bMan = ButtonManager(goToStartCallBack, pauseVideoCallBack, polarity=False)	
	bMan = ButtonManager(goToStartCallBack, muteAudioCallBack, polarity=False)	

	inputLen = getInputDevices()
	prevInputLen = inputLen
	
	# start the shutdown handler function.
	# It will take care of opening and listening on a socket
	# for a "shutdown message".
	shutdownHandlerThread = threading.Thread(target=shutdownHandler)
	shutdownHandlerThread.start()

	# Main loop
	while True:
		# check is someone plugged in a mouse or a keyboard
		if( areThereNewInputsDevices() ):
			# new input devices have been found
 			# script must be stopped in order
			# to let space for the user to work
			# with the Pi

			# quit video player
			videoPlayer.stop() # will exit current vlc window (desktop will be visible)

			# TODO: kill all alive thread
			# find a way to do this

			# exit the python script
			quit()
		else:
			bMan.update()
			#print("MAIN: position {}".format(position) )
			if bUseVideo:
				if position >= 0.99:
					videoPlayer.set_position( 0.0 )
			time.sleep(0.1)
			


if __name__ == '__main__':
	sys.exit( main() )

#End of the script
