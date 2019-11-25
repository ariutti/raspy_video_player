from button import DebounceButton
import RPi.GPIO as GPIO

buttons = []
gpios = [40, 38] #GPIO21, GPIO20
status = [True, True]

class ButtonManager:
	# init method need a callbalck to be called when a special combination of
	# push buttons will be pressed
	
	# polarity: use True if a release should trigger the action on the video
	# use False if it is a push which will trigger it.
	def __init__(self, goToStartCb=None, pauseCb=None, polarity=False):
		self.goToStartCb = goToStartCb
		self.pauseCb = pauseCb
		self.polarity = polarity
		self.precedence = False
		GPIO.setmode( GPIO.BOARD )
		for i, gpio in enumerate(gpios):
			print("BUTTON MANAGER: button {} - gpio {};".format(i, gpio) )
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
			
			# the first button which is pressed after a complete release 
			# phase will obtain a priority
			if self.polarity:
				if s and not self.precedence:
					self.precedence = True
					# call the callback function only if defined
					if self.goToStartCb:
						self.goToStartCb()
					break
			else:
				if not s and not self.precedence:
					self.precedence = True
					# call the callback function only if defined
					if self.goToStartCb:
						self.goToStartCb()
					break
		
		# let's pretend we want to reset the internal state of
		# the button manager (make "precedence" come back to False)
		reset = True
		for s in status:
			# if a button is still beeing released 
			# (pressed in cas we have opposite polarity)
			# we don't need to reset button manager state
			if self.polarity:	
				if s:
					reset = False
					break
			else:
				if not s:
					reset = False
					break
		
		# if we enter this block it means it is time to reset the internal
		# state of the button manager.
		if reset and self.precedence:
			self.precedence = False
			# call the callback function only if defined
			if self.pauseCb:
				self.pauseCb()
		
		
