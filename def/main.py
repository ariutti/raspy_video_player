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
#pathToVideoFile = "/home/pi/Videos/alvanoto.mp4"
pathToVideoFile = "/home/pi/Videos/Aboca/ABOCA_NASCITA_60SEC_ITA_innovazione per la salute.mp4"

# global variable to be used
# for scanning input devices
inputLen = None
prevInputLen = None
process = None
videoPlayer = None

from buttonManager import ButtonManager
		
def goToStartCallBack():
	global videoPlayer
	print("** go to start callback **")
	print( "    start video from position 0.0")
	videoPlayer.set_position(0.0) 
	# the video is in pause so start playing it
	videoPlayer.play()
	
def pauseVideoCallBack():
	global videoPlayer
	print("** pauseVideo callback **")
	print( "    pause video ")
	videoPlayer.pause() 

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

import threading
checkPositionThread = None
position = None
def checkLength():
	global videoPlayer, position
	while 1:
		position = videoPlayer.get_position() # 0.0 - 1.0 position
		#print( "player position: {}".format( position ) )
		time.sleep(0.1)

def main():
	#print( "main" )
	global inputLen, prevInputLen, videoPlayer, position

	# Wait the system to boot up correctly
	#time.sleep(10)
	
	# Open video player
	try:
		print( " load the video " )
		videoPlayer = vlc.MediaPlayer( pathToVideoFile )
		#process = Popen( args, stdin=PIPE, stdout=PIPE )
		#print("This is the omxplayer process id: ",  process.pid )
	except Exception as exc:
		print("something went wrong {}".format(exc) )
		quit()
	
	checkPositionThread = threading.Thread(target=checkLength)
	checkPositionThread.start()
	
	print( "video length {}".format(videoPlayer.get_length() ) )
	
	videoPlayer.audio_set_volume(70)
	videoPlayer.play()
	videoPlayer.toggle_fullscreen() # use it to go fullscreen
	#videoPlayer.video_set_scale(0.5)
	
	bMan = ButtonManager(goToStartCallBack, pauseVideoCallBack, polarity=False)	

	inputLen = getInputDevices()
	prevInputLen = inputLen

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

			# kill all alive thread
			# find a way to do this

			# exit the python script
			quit()
		else:
			bMan.update()
			print("position {}".format(position) )
			if position >= 0.99:
				videoPlayer.set_position( 0.0 )
			time.sleep(0.1)
			


if __name__ == '__main__':
	sys.exit( main() )

#End of the script
