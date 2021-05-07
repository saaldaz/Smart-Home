#!/usr/bin/env python3.5


# NOTE: this example requires PyAudio because it uses the Microphone class

import speech_recognition as sr
import os
import PiRelay
import os
import time
import RPi.GPIO as GPIO
GPIO.setwarnings(False)

state = 1;
GPIO.setmode(GPIO.BCM)
GPIO.setup(2,GPIO.OUT)
GPIO.setup(3,GPIO.OUT)
GPIO.setup(22,GPIO.OUT)
GPIO.setup(17,GPIO.OUT)


while(1):
	
	


	# obtain audio from the microphone
	r = sr.Recognizer()
	with sr.Microphone() as source:
		r.adjust_for_ambient_noise(source)
		print("Say something!")
		audio = r.record(source, duration = 5, offset = None)#r.listen(source)
		#os.system('flite -t "home automation loaded"');
		WIT_AI_KEY = "2EGXOZTN2SVV7XUCSWNJBPQHUBN3IV7W"
		x = r.recognize_wit(audio, key=WIT_AI_KEY)

	# recognize speech using Wit.ai
	# Wit.ai keys are 32-character uppercase alphanumeric strings
	try:
		print("you said " + x)
	except sr.UnknownValueError:
		print("Wit.ai could not understand audio")
	except sr.RequestError as e:
		print("Could not request results from Wit.ai service; {0}".format(e))


	if(x=='light on'):
		file=open("relay1.txt","w")
		file.write("ON")
		file.close()
		GPIO.output(2,False);
	if(x=='light off'):
		file=open("relay1.txt","w")
		file.write("OFF")
		file.close()
		GPIO.output(2,True);
	if(x=='bedroom on'):
				file=open("relay2.txt","w")
				file.write("ON")
				file.close()
				GPIO.output(3,False);
	if(x=='bedroom off'):
		file=open("relay2.txt","w")
		file.write("OFF")
		file.close()
		GPIO.output(3,True);
	if(x=='kitchen on'):
				file=open("relay3.txt","w")
				file.write("ON")
				file.close()
				GPIO.output(22,False);
	if(x=='kitchen off'):
				file=open("relay3.txt","w")
				file.write("OFF")
				file.close()
				GPIO.output(22,True);
	if(x=="garage on"):
		file=open("relay4.txt","w")
		file.write("ON")
		file.close()
		GPIO.output(17,False);
	if(x=="garage off"):
		file=open("relay4.txt","w")
		file.write("OFF")
		file.close()
		GPIO.output(17,True);
