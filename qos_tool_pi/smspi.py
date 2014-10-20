import serial
import time

dongle = serial.Serial(port="/dev/ttyUSB0",baudrate=115200,timeout=10,rtscts=0,xonxoff=0)


dongle.write('AT+CMGD=2,3\r')
time.sleep(1)
dongle.write('AT+CMGF=1\r')
time.sleep(1)
dongle.write('AT+CNMI=2,0,0,0,0\r')
time.sleep(1)
dongle.write('AT+CSMP=49,167,0,0\r')
time.sleep(1)


# Set the telephone number we want to send to
dongle.write('AT+CMGS="+6281514797598"\r')
time.sleep(1)

# Set the message we want to send
dongle.write('The grand gives you more')
time.sleep(1)

# Pass the CTRL+Z character to let the dongle know we're done
dongle.write(chr(26))
time.sleep(1)

out = dongle.read(1024)
print out

# Close the connection
dongle.close()
