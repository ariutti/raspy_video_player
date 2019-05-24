#!/usr/bin/env python3

# Documentation: https://sourceforge.net/p/raspberry-gpio-python/wiki/Inputs/


"""
facendo diversi esperimenti non mi sto trovando affatto bene con la parte del modulo GPIO
che aggancia le callback ai pulsanti.
nonostante io stia usando i pullup interni e anche un condensatore esterno da 100nF comunque, stressando 
molto il pulsante (premendolo e rilasciandolo a ripetizione) ci sono conportamenti strani per cui non detecta 
alcuni fronti di salita o di discesa.

In un futuro esperimento mi proverò ad usare un sistema più rudimentale ma magari più efficacie che legga lo stato del bottone di continuo
e tenga eventualmente traccia di un timer per fare un debouncing automatico.
un po' come la corrispondente classe di Arduino
"""


import threading, readchar, time, sys
import RPi.GPIO as GPIO

gpios = [40, 38, 36]
status = [False, False, False]

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
		print("gianni")
		time.sleep(1)
		
	GPIO.cleanup()
		
	"""	
	myThread = threading.Thread( target=checkInput )
	myThread.start()
	while True:
		if sharedVar:
			print("Trying to quit")
			quit()
		else:
			print( "main thread" )
			time.sleep(1)
	"""
	
	
if __name__ == "__main__":
	sys.exit( main() )
