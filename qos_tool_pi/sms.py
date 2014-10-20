import serial

dongle = serial.Serial(port="/dev/ttyUSB0",baudrate=115200,timeout=0,rtscts=0,xonxoff=0)


def sendatcmd(cmd):
    dongle.write('AT'+cmd+'\r')


# put the dongle into text mode
sendatcmd('+CMGF=1')


# Set the telephone number we want to send to
sendatcmd('+CMGS="+6281514797598"')


# Set the message we want to send
dongle.write('Halo, dari RPi nich')


# Pass the CTRL+Z character to let the dongle know we're done
dongle.write(chr(26))

#rspn = dongle.read(1024)
#print rspn

# Close the connection
dongle.close()
