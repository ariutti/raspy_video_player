#!/usr/bin/env python3

# Documentation: https://sourceforge.net/p/raspberry-gpio-python/wiki/Inputs/
# Arduino Debounce: https://www.arduino.cc/en/Tutorial/Debounce

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

buttons = []
gpios = [40, 38, 36]
status = [False, False, False]

class DebounceButton:
	def __init__(self, channel, debounceDelay):
		self.channel = channel
		self.debounceDelay = debounceDelay / 1000.0
		self.lastDebounceTime = 0
		self.status = GPIO.HIGH
		self.lastStatus = GPIO.HIGH
		self.reading = None
		GPIO.setup( self.channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		
	
	def update(self):
		self.reading = GPIO.input( self.channel )
		#print( self.reading )
		if self.reading != self.lastStatus:
			#print( "reading diverso da last status")
			self.lastDebounceTime = time.time()
			
		if (time.time() - self.lastDebounceTime) > self.debounceDelay :
			#print( "debounce time strascorso")
			# whatever the reading is at, it's been there for longer than the debounce
			# delay, so take it as the actual current state:
			if self.reading != self.status:
				self.status = self.reading
				#print( "Channel {} status: {}".format(self.channel, self.status) )
		
		self.lastStatus = self.reading
		
	def getStatus(self):
		return self.status

		
def main():
	GPIO.setmode( GPIO.BOARD )
	for i, gpio in enumerate(gpios):
		print("button {} - gpio {};".format(i, gpio) )
		buttons.append( DebounceButton(gpio, 50) )
	

	while True:
		for i, b in enumerate(buttons):
			b.update()
			status[i] = b.getStatus()
		print( status )
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
