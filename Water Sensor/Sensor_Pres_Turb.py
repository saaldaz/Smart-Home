from datetime import datetime
import RPi.GPIO as GPIO
import busio
import digitalio
import board
import time, sys
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import MySQLdb

spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs  = digitalio.DigitalInOut(board.D5)
mcp = MCP.MCP3008(spi, cs)

dbHost = 'localhost'
dbName = 'Data'
dbUser = 'admin'
dbPass = 'cpp'
time_new = 0.0
sample = 10.0

print('Monitoring Start Time: ', str(time.asctime(time.localtime(time.time()))))
sample = int(input('Input desired sample interval in second(s): '))
print('Samples every ', sample, ' second(s)')
print('CTRL+C to exit')

while True:
    dbConnection = MySQLdb.connect(host=dbHost, user=dbUser, passwd=dbPass, db=dbName)
    cur = dbConnection.cursor(MySQLdb.cursors.DictCursor)
    time_new = time.time() + sample
    while time.time() <= time_new:
        try:
            None
            print(end='')
        except KeyboardInterrupt:
            GPIO.cleanup()
            print('Done')
            sys.exit()
            
    chan0 = AnalogIn(mcp, MCP.P0)
    chan1 = AnalogIn(mcp, MCP.P1)
    volt0 = chan0.voltage
    volt1 = chan1.voltage
    ntu = round((-909.9656*volt0) + 3000,3)
    psi = round((50.0*volt1) - 26.1,3)

    mySql_insert_query="INSERT INTO Sensor_Pres_Turb(Pressure,Turbidity,Time) Values(%s,%s,%s)"
    val=(psi,ntu,datetime.now())
    cur.execute(mySql_insert_query,val)
    dbConnection.commit()
    
    #print('Pres Voltage: ' + str(round(chan1.voltage,3)) + 'V')
    #print('Turb Voltage: ' + str(round(chan0.voltage,3)) + 'V')
    print('Pressure: ', str(psi), ' psi')
    print('Turbidity: ', ntu, ' NTU')
    print(time.asctime(time.localtime(time.time())), '\n')
    
GPIO.cleanup()
print('Done')
