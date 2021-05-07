#!/usr/bin/env python3
"""aqi.py: Air Quality Index Monitor"""

# owned
__author__ = 'Ram Patel'
__copyright__ = 'Copyright 2021, Air Quality Index Monitor'
__credits__ = ['Ram Patel']
__license__ = 'MIT'
__version__ = '0.1.0'
__maintainer__ = 'Ram Patel'
__email__ = 'patram949@gmail.com'
__status__ = 'Dev'

import serial, time, configparser
from colorama import Fore, Back, Style
from serial import Serial
from texttable import Texttable
from tqdm import tqdm
from ISStreamer.Streamer import Streamer
from Adafruit_IO import Client as adaClient
from pushover import Client as poClient

def alert(pmtwofive, pmten):
    po = poClient(config['pushover']['user_key'], api_token=config['pushover']['api_token'])
    if (pmtwofive <= 12) and (pmten <= 54):
        print(Fore.GREEN + '--- Air quality levels are good. --- ' + Style.RESET_ALL)
    elif (pmtwofive > 12) or (pmten > 54):  
        if (pmtwofive > 12):
            print(Fore.RED + '!!! PM2.5 air quality reading above acceptable levels; triggering alert !!! ' + Style.RESET_ALL)
            po.send_message("!!! PM2.5 AQI above acceptable level; check environment !!!", title="PM2.5 AQI Alert")
        if (pmten > 54):
            print(Fore.RED + '!!! PM10 air quality reading above acceptable levels; triggering alert !!! ' + Style.RESET_ALL)
            po.send_message("!!! PM2.5 AQI above acceptable level; check environment !!!", title="PM10 AQI Alert")
    else:
        print(Fore.RED + '!!! Unknown AQI reading; triggering alert !!! ' + Style.RESET_ALL)
        po.send_message("!!! Unknown AQI reading; check monitor !!!", title="AQI Unknown Alert")
    

def publish(svc, pmtwofive, pmten):
    print(Back.GREEN + '\nStreaming to '+ svc + Style.RESET_ALL)
    if svc == 'initialstate':
        initialstate(pmtwofive, pmten)
    elif svc == 'adafruitio':
        adafruitio(pmtwofive, pmten)
    elif svc == 'both':
        initialstate(pmtwofive, pmten)
        adafruitio(pmtwofive, pmten)
    else: 
        print('Invalid Service')

def initialstate(pmtwofive, pmten):
    streamer.log("PM_2.5", pmtwofive)
    streamer.log("PM_10", pmten)
    # flush data (force the buffer to empty and send)
    streamer.flush()
    # close the stream
    streamer.close()

def adafruitio(pmtwofive, pmten):
    pmtwofive_feed = aio.feeds(config['adafruit_io']['pmtwofive_feed'])
    pmten_feed = aio.feeds(config['adafruit_io']['pmten_feed'])
    aio.send(pmtwofive_feed.key, pmtwofive)
    aio.send(pmten_feed.key, pmten)

def main():
    while True:
        data = []
        for index in range(0,10):
            datum = ser.read()
            data.append(datum)
        pmtwofive = int.from_bytes(b''.join(data[2:4]), byteorder='little') / 10   
        pmten = int.from_bytes(b''.join(data[4:6]), byteorder='little') / 10
        publish(config['local']['services'], pmtwofive, pmten)
        t = Texttable()
        t.add_rows([['Desc', 'Metric'], ['PM2.5', pmtwofive], ['PM10', pmten]])
        print(t.draw())
        alert(pmtwofive, pmten)
        # visual cycle time
        for i in tqdm(range(cycle_time)):
            time.sleep(1)
    
if __name__ == '__main__':
    # read and parse config file
    config = configparser.ConfigParser()
    config.read('config.ini')
    config.sections()
    # create a Streamer instance
    streamer = Streamer(bucket_name=config['initialstate']['is_bucket_name'], bucket_key=config['initialstate']['is_bucket_key'], access_key=config['initialstate']['is_access_key'])
    # create a adafruit.io instance
    aio = adaClient(config['adafruit_io']['adafruitio_username'], config['adafruit_io']['adafruitio_key'])
    # set port for air quality monitor
    ser = serial.Serial(config['local']['device'])
    # set cycle time
    cycle_time = int(config['local']['cycle_time'])    
    main()
