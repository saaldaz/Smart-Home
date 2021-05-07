from datetime import datetime
import RPi.GPIO as GPIO
import time, sys, os, glob
import MySQLdb


os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

temp_sensor = '/sys/bus/w1/devices/28-01204f50cbf9/w1_slave'


GPIO.setmode(GPIO.BOARD)
inpt = 13
GPIO.setup(inpt, GPIO.IN)
global dbHost
global dbName
global dbUser
global dbPass
	
dbHost = 'localhost'
dbName = 'Data'
dbUser = 'admin'
dbPass = 'cpp'
minutes = 0
constant = 0.006
time_new = 0.0
rpt_int = 10

##Temperature Sensor
def read_temp_raw():
    f = open(temp_sensor, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c

##Flow Sensor
global rate_cnt, tot_cnt
rate_cnt = 0
tot_cnt = 0

def Pulse_cnt(inpt_pin):
    global rate_cnt, tot_cnt
    rate_cnt += 1
    tot_cnt += 1

GPIO.add_event_detect(inpt, GPIO.FALLING,
                      callback = Pulse_cnt,bouncetime = 10)


#Main
print('Monitoring Start Time', str(time.asctime(time.localtime(time.time()))))
rpt_int = int(input('Input desired report interval in seconds '))
print('Reports every ', rpt_int, ' seconds')
print('CTRL+C to exit')

while True:
    dbConnection = MySQLdb.connect(host=dbHost, user=dbUser, passwd=dbPass, db=dbName)
    cur = dbConnection.cursor(MySQLdb.cursors.DictCursor)
    time_new = time.time() + rpt_int
    rate_cnt = 0
    while time.time() <= time_new:
        try:
            None
            print(end='')
        except KeyboardInterrupt:
            GPIO.cleanup()
            print('Done')
            sys.exit()
    minutes += 1

    LperM = round(((rate_cnt*constant)/(rpt_int/60)), 2)
    TotLit = round(tot_cnt*constant, 1)

    mySql_insert_query="INSERT INTO Sensor_Flow_Temp(Flow_Rate,Total_Liters,Temperature,Time) Values(%s,%s,%s,%s)"
    val=(LperM,TotLit,read_temp(),datetime.now())

    cur.execute(mySql_insert_query,val)
    dbConnection.commit()                                       

    print('\nLiters/min: ', LperM)
    print('Total Liters: ', TotLit)
    print('Temperature (Celsius): ', read_temp())
    print(time.asctime(time.localtime(time.time())), '\n')

GPIO.cleanup()
print('Done')
