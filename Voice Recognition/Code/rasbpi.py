#!/usr/bin/python3.5
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


while(state):

    
    device1 = open('relay1.txt','r');
    device2 = open('relay2.txt','r');
    device3 = open('relay3.txt','r');
    device4 = open('relay4.txt','r');
    
    dev1 = device1.read();
    dev2 = device2.read();
    dev3 = device3.read();
    dev4 = device4.read();

    if (dev1=='ON'):
        GPIO.output(2,False);
    if (dev1=='OFF'):
        GPIO.output(2,True);

    if(dev2=='ON'):
        GPIO.output(3,False);
    if(dev2=='OFF'):
         GPIO.output(3,True);
  
    if(dev3=='ON'):
        GPIO.output(22,False);
    if(dev3=='OFF'):
         GPIO.output(22,True);

    if(dev4=='ON'):
        GPIO.output(17,False);
    if(dev4=='OFF'):
         GPIO.output(17,True);
         
    time.sleep(2);




