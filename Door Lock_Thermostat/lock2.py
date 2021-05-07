import sys
import MySQLdb
from threading import Thread
import threading
import time
import RPi.GPIO as GPIO
import json
from subprocess import call
import tkinter as tk
from tkinter import ttk
from random import randint
from evdev import InputDevice
from select import select
from twilio.rest import Client
import os

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(13,GPIO.OUT)


def Thermostat():
         call(['python3', 'example.py'])
         sys.exit()


                
class Fullscreen_Window:
        
        global dbHost
        global dbName
        global dbUser
        global dbPass
        
        dbHost = 'localhost'
        dbName = 'door_lock'
        dbUser = 'root'
        dbPass = 'Rassberry123'
        
        def __init__(self):
                self.tk = tk.Tk()
                self.tk.title("Two-Factor Authentication Security Door Lock")
                self.frame = tk.Frame(self.tk)
                self.frame.grid()
                self.tk.columnconfigure(0, weight=1)
                
                self.tk.attributes('-zoomed', True)
                self.tk.attributes('-fullscreen', True)
                self.state = True
                self.tk.bind("<F11>", self.toggle_fullscreen)
                self.tk.bind("<Escape>", self.end_fullscreen)
                
                self.tk.config(cursor="none")
                
                self.show_idle()
                
                t = Thread(target=self.listen_rfid)
                t.daemon = True
                t.start()
                
        def show_idle(self):
                self.welcomeLabel = ttk.Label(self.tk, text="Please Present\nYour Token")
                self.welcomeLabel.config(font='size, 20', justify='center', anchor='center')
                self.welcomeLabel.grid(sticky=tk.W+tk.E, pady=210)
                self.TemperatureButton =tk.Button(self.tk, text ='Thermostat', font ='size, 10', command = Thermostat, bg='gray',height=2, justify='center', anchor='center', width=6)
                self.TemperatureButton.grid(row=0, sticky=tk.N)
                
                
        def pin_entry_forget(self):
                self.validUser.grid_forget()
                self.enterPINlabel.grid_forget()
                count = 0
                while (count < 12):
                        self.btn[count].grid_forget()
                        count += 1
                
        def returnToIdle_fromPINentry(self):
                self.pin_entry_forget()
                self.show_idle()
                
        def returnToIdle_fromPINentered(self):
                self.PINresultLabel.grid_forget()
                self.show_idle()
                
        def returnToIdle_fromAccessGranted(self):
                GPIO.output(13,GPIO.HIGH)
                self.SMSresultLabel.grid_forget()
                self.show_idle()
                
        
        def toggle_fullscreen(self, event=None):
                self.state = not self.state  # Just toggling the boolean
                self.tk.attributes("-fullscreen", self.state)
                return "break"


        def end_fullscreen(self, event=None):
                self.state = False
                self.tk.attributes("-fullscreen", False)
                return "break"

            
        def listen_rfid(self):
                global pin
                global accessLogId
                
                keys = "X^1234567890XXXXqwertzuiopXXXXasdfghjklXXXXXyxcvbnmXXXXXXXXXXXXXXXXXXXXXXX"
                dev = InputDevice('/dev/input/event0')
                rfid_presented = ""

                while True:
                        r,w,x = select([dev], [], [])
                        for event in dev.read():
                                if event.type==1 and event.value==1:
                                                if event.code==28:
                                                        dbConnection = MySQLdb.connect(host=dbHost, user=dbUser, passwd=dbPass, db=dbName)
                                                        cur = dbConnection.cursor(MySQLdb.cursors.DictCursor)
                                                        cur.execute("SELECT * FROM access_list WHERE rfid_code = '%s'" % (rfid_presented))
                                                        
                                                        if cur.rowcount != 1:
                                                                self.welcomeLabel.config(text="ACCESS DENIED")
                                                                
                                                                # Log access attempt
                                                                cur.execute("INSERT INTO access_log SET rfid_presented = '%s', rfid_presented_datetime = NOW(), rfid_granted = 0" % (rfid_presented))
                                                                dbConnection.commit()
                                                                
                                                                time.sleep(3)
                                                                self.welcomeLabel.grid_forget()
                                                                self.show_idle()
                                                        else:
                                                                user_info = cur.fetchone()
                                                                userPin = user_info['pin']
                                                                self.welcomeLabel.grid_forget()
                                                                self.validUser = ttk.Label(self.tk, text="Welcome\n %s!" % (user_info['name']), font='size, 15', justify='center', anchor='center')
                                                                self.validUser.grid(columnspan=3, sticky=tk.W+tk.E)
                                                                
                                                
                                              
                                                                self.enterPINlabel = ttk.Label(self.tk, text="Please enter your PIN:", font='size, 18', justify='center', anchor='center')
                                                                self.enterPINlabel.grid(columnspan=3, sticky=tk.W+tk.E)

                                                               
                                                                pin = ''
                                                                
                                                                keypad = [
                                                                        '1', '2', '3',
                                                                        '4', '5', '6',
                                                                        '7', '8', '9',
                                                                        '*', '0', '#',
                                                                ]
                                                                
                                                                # create and position all buttons with a for-loop
                                                                # r, c used for row, column grid values
                                                                r = 4
                                                                c = 0
                                                                n = 0
                                                                # list(range()) needed for Python3
                                                                self.btn = list(range(len(keypad)))
                                                                for label in keypad:
                                                                        # partial takes care of function and argument
                                                                        #cmd = partial(click, label)
                                                                        # create the button
                                                                        self.btn[n] = tk.Button(self.tk, text=label, font='size, 18', width=4, height=1, command=lambda digitPressed=label:self.codeInput(digitPressed, userPin, user_info['sms_number']))
                                                                        # position the button
                                                                        self.btn[n].grid(row=r, column=c, ipadx=10, ipady=10)
                                                                        # increment button index
                                                                        n += 1
                                                                        # update row/column position
                                                                        c += 1
                                                                        if c > 2:
                                                                                c = 0
                                                                                r += 1
                                                                

                                                                
                                                                # Log access attempt
                                                                cur.execute("INSERT INTO access_log SET rfid_presented = '%s', rfid_presented_datetime = NOW(), rfid_granted = 1" % (rfid_presented))
                                                                dbConnection.commit()
                                                                accessLogId = cur.lastrowid
                                                                
                                                                self.PINentrytimeout = threading.Timer(10, self.returnToIdle_fromPINentry)
                                                                self.PINentrytimeout.start()
                                                                
                                                                self.PINenteredtimeout = threading.Timer(5, self.returnToIdle_fromPINentered)


                                                
                                                        rfid_presented = ""
                                                        dbConnection.close()

                                                        
                                                else:
                                                        rfid_presented += keys[ event.code ]

        def codeInput(self, value, userPin, mobileNumber):
                global accessLogId
                global pin
                global smsCodeEntered
                pin += value
                pinLength = len(pin)
                
                self.enterPINlabel.config(text="Digits Entered: %d" % pinLength)
                
                if pinLength == 6:
                        self.PINentrytimeout.cancel()
                        self.pin_entry_forget()
                        
                        if pin == userPin:
                                pin_granted = 1
                        else:
                                pin_granted = 0
                        
                        # Log access attempt
                        dbConnection = MySQLdb.connect(host=dbHost, user=dbUser, passwd=dbPass, db=dbName)
                        cur = dbConnection.cursor()
                        cur.execute("UPDATE access_log SET pin_entered = '%s', pin_entered_datetime = NOW(), pin_granted = %s, mobile_number = '%s' WHERE access_id = %s" % (pin, pin_granted, mobileNumber, accessLogId))
                        dbConnection.commit()
                        
                        if pin == userPin:
                                self.SMSresultLabel = ttk.Label(self.tk, text="Thank You,\nAccess Granted")
                                self.SMSresultLabel.config(font='size, 20', justify='center', anchor='center')
                                self.SMSresultLabel.grid(columnspan=3, sticky=tk.W+tk.E, pady=210)
                                
                                GPIO.output(13,GPIO.LOW)
                                
                                self.doorOpenTimeout = threading.Timer(10, self.returnToIdle_fromAccessGranted)
                                self.doorOpenTimeout.start()
                                
                        else:
                                self.PINresultLabel = ttk.Label(self.tk, text="Incorrect PIN\nEntered!")
                                self.PINresultLabel.config(font='size, 20', justify='center', anchor='center')
                                self.PINresultLabel.grid(sticky=tk.W+tk.E, pady=210)
                                self.PINenteredtimeout.start()
                                


if __name__ == '__main__':
        w = Fullscreen_Window()
        
        w.tk.mainloop()

