#!/usr/bin/env python3

# Documentation: https://sourceforge.net/p/raspberry-gpio-python/wiki/Inputs/
# Arduino Debounce: https://www.arduino.cc/en/Tutorial/Debounce


import threading, readchar, time, sys
from buttonManager import ButtonManager
		
def goToStartCallBack():
	print("go to start callbak")
		
def main():
	bMan = ButtonManager(goToStartCallBack)
	
	while True:
		bMan.update()
		time.sleep(0.1)
	
	







"""
def myOnPressCallback(channel):
	if GPIO.input(channel) == GPIO.LOW:
		print("channel {} low".format(channel) )
	elif GPIO.input(channel) == GPIO.HIGH:
		print("channel {} high".format(channel) )
	


def main():
	GPIO.setmode( GPIO.BOARD )
	for channel in gpios:
		print( channel )
		GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		GPIO.add_event_detect(channel, GPIO.BOTH, callback=myOnPressCallback, bouncetime=200)
		#GPIO.add_event_detect(channel, GPIO.RISING, callback=myOnReleaseCallback, bouncetime=5000)
		
	while True:
		print("gianni {}".format( time.time() ))
		time.sleep(1)
		
	GPIO.cleanup()
"""
	
if __name__ == "__main__":
	sys.exit( main() )
