from button import DebounceButton
import RPi.GPIO as GPIO

buttons = []
gpios = [40, 38] #GPIO21, GPIO20
status = [True, True]

class ButtonManager:
	# init method need a two callbalcks
	# 1. the first one will be used to trigger an action (defined in main file)
	#    when at least one audio receiver is lifted up by a user;
	# 2. The second one will be used to trigger some action when both the
	#    audio receivers will be hanged up.

	# polarity: use True if a release should trigger the action on the video
	# use False if it is a push which will trigger it.
	def __init__(self, callBack_1=None, callBack_2=None, polarity=False):
		self.callBack_1 = callBack_1
		self.callBack_2 = callBack_2
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
		# check if there's at least one button pressed (one audio receiver lifted)
		for s in status:
			# if so and no other button pressed from before (precedence == False)
			# exit the loop: we have already found what we were looking for.

			# The button which is lifted as the first one will obtain a priority
			if self.polarity:
				if s and not self.precedence:
					self.precedence = True
					# call the callback function only if defined
					if self.callBack_1:
						self.callBack_1()
					break
			else:
				if not s and not self.precedence:
					self.precedence = True
					# call the callback function only if defined
					if self.callBack_1:
						self.callBack_1()
					break

		# When both the audio receivers are hanged up, we should reset the internal
		# state of the button manager (make "precedence" come back to False)
		reset = True
		for s in status:
			# if a button is still beeing released
			# (pressed in case we have opposite polarity)
			# we don't need to reset button manager state
			if self.polarity:
				if s:
					reset = False
					break
			else:
				if not s:
					reset = False
					break


		if reset and self.precedence:
			# if we are here it means it's time to reset the internal
			# state of the button manager.
			self.precedence = False
			# call the callback function only if defined
			if self.callBack_2:
				self.callBack_2()
