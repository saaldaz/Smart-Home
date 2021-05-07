#! /usr/bin/python3

# Imports
import RPi.GPIO as GPIO
import time
import requests

# Set the GPIO naming convention
GPIO.setmode(GPIO.BCM)

# Turn off GPIO warnings
GPIO.setwarnings(False)

# Set a variable to hold the GPIO Pin identity
pinpir = 17


GPIO.setup(pinpir, GPIO.IN)

currentstate = 0
previousstate = 0

try:
	print("Waiting for Motion detector to settle ")
	
	while GPIO.input(pinpir) == 1:
	
		currentstate = 0

	print("    Ready")
	
	
	while True:
	
		# Read PIR state
		currentstate = GPIO.input(pinpir)

		# If the PIR is triggered
		if currentstate == 1 and previousstate == 0:
		
			print("Motion detected!")
			
			
			r = requests.post('https://maker.ifttt.com/trigger/motion_detected/with/key/fh_xG0_AJDX3pejm-iWM0qvCQMnRzHIVnTRIz_PE8v-', params={"value1":"none","value2":"none","value3":"none"})
			
			
			previousstate = 1
			
			#Wait 60 seconds before looping again
			print("Waiting 15 seconds")
			time.sleep(15)
			
		
		elif currentstate == 0 and previousstate == 1:
		
			print("Ready")
			previousstate = 0


		time.sleep(0.01)

except KeyboardInterrupt:
	print("    Quit")


	GPIO.cleanup()


