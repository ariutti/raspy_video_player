#!/usr/bin/env python3

# VLC PLAYER playlist test


#Import the required modules
import smbus, time, shlex, glob, random, sys
from subprocess import Popen, PIPE

# see: https://git.videolan.org/?p=vlc/bindings/python.git;a=blob;f=generated/3.0/vlc.py;h=e3245a5116946a4b52cadf5642441daa97af022d;hb=HEAD 
# and: https://olivieraubert.net/vlc/python-ctypes/doc/vlc.MediaPlayer-class.html
# for reference

import vlc
mediaList = None
mediaListPlayer = None
mediaPlayer = None
pathToVideoFile1 = "/home/pi/Videos/Aboca/ABOCA_NASCITA_60SEC_ITA_innovazione per la salute.mp4"
pathToVideoFile2 = "/home/pi/Videos/Aboca/ABOCA_NASCITA_60SEC_ENG.mp4"


# global variable to be used
# for scanning input devices
inputLen = None
prevInputLen = None
process = None

#from buttonManager import ButtonManager
		
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
	global inputLen, prevInputLen, mediaList, mediaListPlayer, mediaPlayer, position

	# Wait the system to boot up correctly
	#time.sleep(10)
	
	# Open video player
	try:
		print( " load the video " )
		# create a list of media
		mediaList = vlc.MediaList()
		# and add itmes to it
		mediaList.add_media( pathToVideoFile1 )
		mediaList.add_media( pathToVideoFile2 )
		# create the player which will play that list
		mediaListPlayer = vlc.MediaListPlayer()
		mediaListPlayer.set_media_list( mediaList  )
	except Exception as exc:
		print("something went wrong {}".format(exc) )
		quit()
	
	mediaListPlayer.set_playback_mode( vlc.PlaybackMode.loop )
	mediaListPlayer.play_item( mediaList.item_at_index(0) )
	mediaPlayer = mediaListPlayer.get_media_player()
	mediaPlayer.toggle_fullscreen()
	
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
			#print("position {}".format(position) )
			#if position >= 0.99:
			#	videoPlayer.set_position( 0.0 )
			time.sleep(0.1)
			


if __name__ == '__main__':
	sys.exit( main() )

#End of the script
