import serial
import time

dongle = serial.Serial(port="/dev/ttyUSB0",baudrate=115200,timeout=10,rtscts=0,xonxoff=0)

dongle.write('ATD123;\r')
time.sleep(3)
dongle.write('AT^DDSETEX=2\r')
time.sleep(5)
dongle.close()
