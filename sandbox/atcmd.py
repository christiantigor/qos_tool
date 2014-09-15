import serial, sys

#setup connection to dongle
dongle = serial.Serial(port="/dev/ttyUSB0",baudrate=115200,timeout=10,rtscts=0,xonxoff=0)

#define at command format
def sendatcmd(cmd):
    dongle.write('AT'+cmd+'\r')

def main():
    while 1:
        input = raw_input('\n=>')
        if input == 'quit':
            print 'Quitting'
            sys.exit(0)
        elif input == 'end':
            print 'ctrl+z'
            dongle.write(chr(26))
            rspn = dongle.read(2048)
            print rspn
            #wait for response (looping here)
            rspn1 = dongle.read(2048)
            print rspn1
            continue
        else:
            sendatcmd(input)
            rspn = dongle.read(2048)
            print rspn
            continue

if __name__ == '__main__':
    main()
