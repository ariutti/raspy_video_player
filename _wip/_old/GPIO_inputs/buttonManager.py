from button import DebounceButton
import RPi.GPIO as GPIO

buttons = []
gpios = [40, 38, 36]
status = [False, False, False]

class ButtonManager:
	# init method need a callbalck to be called when a special combination of
	# push buttons will be pressed
	def __init__(self, goToStartCb):
		self.goToStartCb = goToStartCb
		self.precedence = False
		GPIO.setmode( GPIO.BOARD )
		for i, gpio in enumerate(gpios):
			print("button {} - gpio {};".format(i, gpio) )
			buttons.append( DebounceButton(gpio, 50) )
		
			
	def update(self):
		for i, b in enumerate(buttons):
			b.update()
			status[i] = b.getStatus()
		#print( status )
		self.check()
		
		
	def check(self):
		# check if there's at least on button pressed
		for s in status:	
			#if so and no other button pressed from before
			# (precedence == False) exit the loop: we have found 
			# what we were looking for
			if s and not self.precedence:
				self.precedence = True
				self.goToStartCb()
				break
				
		reset = True
		for s in status:	
			if s:
				reset = False
				break
		if reset and self.precedence:
			self.precedence = False
		
		
