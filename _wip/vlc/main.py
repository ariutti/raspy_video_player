#!/usr/bin/env python3

# see https://git.videolan.org/?p=vlc/bindings/python.git;a=blob;f=generated/3.0/vlc.py;h=e3245a5116946a4b52cadf5642441daa97af022d;hb=HEAD for reference

import vlc, time

# player is an instance of MediaPlayer
player = vlc.MediaPlayer("/home/pi/Documents/repos/raspy_video_player/_wip/nuovi_test/vlc/alvanoto.mp4")
#player = vlc.MediaPlayer("/home/nicola/Documenti/_sketchbooks/python_scripts/vlc/alvanoto.mp4")
print("file loaded and playing")
#player.toggle_fullscreen() # use it to go fullscreen

# use below function to play the movie
player.play()

# use below function after the video is in play
# set position between 0.0 and 1.0
print( "start video from position 0.5")
player.set_position(0.5) 

# get the actual volume of the vlc player (0-100)
# return: 0 if the volume was set, -1 if it was out of range.
print( "audio volume is {}".format(player.audio_get_volume() ) )

time.sleep( 2 )

# use below function to set a new audio volume for the player
player.audio_set_volume(70)

print( "audio volume now is {}".format( player.audio_get_volume() ) )

time.sleep(2)

# prior to put the video in pause it have to play for a minimum time
print("pause")
player.pause()

time.sleep(2)

# calling pause two time will restart the playback
print("un-pause")
player.pause()

time.sleep(2)

print("going back to position 0")
player.set_position(0) # use this method to restart the playback from the beginning

time.sleep(2)

print("Player stop")
player.stop() # will exit current vlc window (desktop will be visible)


"""
time.sleep(10)
player.pause()
print("paused")

for i in range(4):
	print(i)
	print("cycle")
	player.pause()
	time.sleep(3)
	
#print("stop")
#player.stop() # will exit current vlc window (desktop will be visible)
player.set_position(0)
print("prev chapter")

time.sleep(10)
player.play()
print("playing")

for i in range(4):
	print(i)
	print("cycle")
	player.pause()
	time.sleep(3)


player.stop()
print("stop")
"""
