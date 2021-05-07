from tkinter import *
import tkinter as tk
import tkinter.font
import time as tm
import Adafruit_DHT
from subprocess import call
import RPi.GPIO as GPIO

##Hardware##
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 21
GPIO.setup(16,GPIO.OUT)
GPIO.setup(13,GPIO.OUT)
GPIO.setup(20,GPIO.OUT)
GPIO.setup(26,GPIO.OUT)
GPIO.output(16, True)
GPIO.output(20, True)
GPIO.output(26, True)
GPIO.output(13, True)
temp=0
settemp=0

##window##
win = tk.Tk()
win.title("Temperature")
app_width =300
app_height =200

screen_width = win.winfo_screenwidth()
screen_height = win.winfo_screenheight()

x =(screen_width/2)-(app_width/2)
y=(screen_height/2)-(app_height/2)
win.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')
myFont= tkinter.font.Font(family = 'Helvetica', size =12, weight="bold") 
##variable##


##Event Function##

def cel():
        global temp
        humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
        temp = (temperature)%100
        current_time=tm.strftime('%I:%M:%S:%p ')
        the_label.configure(text=current_time+str(temp)+" C")
        
def far():
        global temp
        humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
        temp = (temperature * 9/5.0 + 32)%100
        current_time=tm.strftime('%I:%M:%S:%p ')
        the_label.configure(text=current_time+str(temp)+" F")
        
def warm():
        global temp
        global settemp
        humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
        temp = (temperature * 9/5.0 + 32)
        settemp=int(FTempcontrol.get())
        if settemp>temp:
                GPIO.output(16,False)
        else:
                GPIO.output(16,True)
        
def cold():
        global temp
        global settemp
        humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
        temp = (temperature * 9/5.0 + 32)
        settemp=int(FTempcontrol.get())
        if settemp<temp:
                GPIO.output(20,False)
        else:
                GPIO.output(20,True)
       
def wind():
        GPIO.output(26,False)

def off():
        GPIO.output(16, True)
        GPIO.output(20, True)
        GPIO.output(26, True)
        
def READ():
    global temp
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    temp =(temperature * 9/5.0 + 32)
    current_time=tm.strftime('%I:%M:%S:%p ')
    the_label.configure(text=current_time+str(temp)+" F")
    temp =(temperature)
    current_time=tm.strftime('%I:%M:%S:%p ')
    the_label2.configure(text=current_time+str(temp)+" C")
    
    
def exitProgram():
    call(['python3','lock2.py'])
    win.destroy()
     
    
def read_every_second():
    READ()
    win.after(1000, read_every_second)
    
##Widgets##    
the_label = tk.Label (win, text="", fg="black", bg="white", font="36")
the_label.grid(row=3, sticky=tk.N)

the_label2 = tk.Label (win, text="", fg="black", bg="white", font="36")
the_label2.grid(row=4, sticky=tk.N)

heat= tk.Button(win, text ='Heat', font =myFont, command= warm, bg='red',height=1, width=1)
heat.grid(row =0, sticky=tk.W)

cool= tk.Button(win, text ='Cool', font =myFont, command= cold, bg='blue',height=1, width=1)
cool.grid(row =0, sticky=tk.E)

fan= tk.Button(win, text ='Fan', font =myFont, command=wind, bg='cyan',height=1, width=1)
fan.grid(row =0, sticky=tk.N)

off= tk.Button(win, text ='Off', font =myFont, command=off, bg='purple',height=1, width=1)
off.grid(row =1, sticky=tk.S)

celsius= tk.Button(win, text ='C', font =myFont, command= cel, bg='purple',height=1, width=1)
celsius.grid(row =1, sticky=tk.W)
farienheit = tk.Button(win, text ='F', font =myFont, command= far, bg='green',height=1, width=1)
farienheit.grid(row =1, sticky=tk.E)


FTempcontrol = tk.Spinbox(win,from_=0, to=100,increment=1 ,width=5)
FTempcontrol.grid(row =2, sticky=tk.E)
exitButton = tk.Button(win, text ='Exit', font =myFont, command = exitProgram, bg='cyan',height=1, width=6)
exitButton.grid(row =5, sticky=tk.W)




##mainloop##
read_every_second()
win.mainloop()

