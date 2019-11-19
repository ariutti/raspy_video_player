#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time

myPins = [40, 38]

GPIO.setmode(GPIO.BOARD) #GPIO.BCM

for pin in myPins:
	GPIO.setup( pin, GPIO.IN, pull_up_down=GPIO.PUD_UP ) # enable the pullup


try:
	while(1):
		#read the input
		values = [GPIO.input(pin) for pin in myPins]
		print( values )
		time.sleep(0.25)
		"""
		for pin in myPins:
			value = GPIO.input( myPin )
			print( value )
			time.sleep(0.25)
		"""
except:
	print("cleanup")
	GPIO.cleanup()
	
	
	
