import serial
import re
import sys
from simplesms import pdu as gsmpdu

#functions to get sim card balance from various operator

#XL
def xlBalance(ttyUsbx):
    try:
        p = "/dev/"+ttyUsbx
        num = "*123#"
        enc = gsmpdu.encode(num)
        cmd = 'AT+CUSD=1,"' + enc + '",15\r'
        modem = serial.Serial(port=p,baudrate=115200,timeout=5,rtscts=0,xonxoff=0)
        modem.write("AT+CUSD=2\r")
        modem.write(cmd)
        rspn = modem.read(1024)
        pattern = r'"([A-Za-z0-9_]*)"'
        texts = re.findall(pattern,rspn)
        dec = gsmpdu.decode(texts[1])
        balMatcher = re.compile("Pulsa (\d+)")
        balance = balMatcher.findall(dec)
        return balance[0]
        modem.close()
    except:
        print "!!! XL Balance error !!!"
        modem.close()
        sys.exit(1)

#TELKOMSEL
def telkomselBalance(ttyUsbx):
    try:
        p = "/dev/"+ttyUsbx
        num = "*888#"
        enc = gsmpdu.encode(num)
        cmd = 'AT+CUSD=1,"' + enc + '",15\r'
        modem = serial.Serial(port=p,baudrate=115200,timeout=5,rtscts=0,xonxoff=0)
        modem.write("AT+CUSD=2\r")
        modem.write(cmd)
        rspn = modem.read(1024)
        pattern = r'"([A-Za-z0-9_]*)"'
        texts = re.findall(pattern,rspn)
        dec = gsmpdu.decode(texts[1])
        balPattern = r'Rp.([0-9_]*).'
        balance = re.findall(balPattern,dec)
        return balance[0]
        modem.close()
    except:
        print "!!! TELKOMSEL Balance error !!!"
        modem.close()
        sys.exit(1)

#INDOSAT
def indosatBalance(ttyUsbx):
    try:
        p = "/dev/"+ttyUsbx
        num = "*555#"
        enc = gsmpdu.encode(num)
        cmd = 'AT+CUSD=1,"' + enc + '",15\r'
        modem = serial.Serial(port=p,baudrate=115200,timeout=5,rtscts=0,xonxoff=0)
        modem.write("AT+CUSD=2\r")
        modem.write(cmd)
        rspn = modem.read(1024)
        pattern = r'"([A-Za-z0-9_]*)"'
        texts = re.findall(pattern,rspn)
        dec = gsmpdu.decode(texts[1])
        balPattern = r'Rp.([0-9_]*).'
        balance = re.findall(balPattern,dec)
        return balance[0]
        modem.close()
    except:
        print "!!! INDOSAT Balance error !!!"
        modem.close()
        sys.exit(1)

#3
