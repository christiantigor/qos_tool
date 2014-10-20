import re, serial, sys, time, uuid
import simbalance

#network operator
def operator(ttyUsbx):
    try:
        p = "/dev/"+ttyUsbx
        modem = serial.Serial(port=p,baudrate=115200,timeout=0.5,rtscts=0,xonxoff=0)
        modem.write("AT+COPS?\r")
        rspn = modem.read(1024)
        pattern = r'"([A-Za-z0-9_]*)"'
        operator = re.search(pattern,rspn)
        return operator.group()
        modem.close() 
    except:
        print "!!! get network operator error  !!!"
        modem.close()
        sys.exit(1)

#sim card balance
def balance(operator,ttyUsbx):
    try:
        if operator == '"XL"':
            return simbalance.xlBalance(ttyUsbx)
        elif operator == '"Telkomsel"':
            pass
        else:
            print "operator unknown"
            sys.exit(1)
    except:
        print "!!! get sim card balance error  !!!"
        sys.exit(1)

#get sms delivery percentage
def smsdelivery(phoneNum,trial,ttyUsbx):
    try:
        p = "/dev/"+ttyUsbx
        modem = serial.Serial(port=p,baudrate=115200,timeout=5,rtscts=0,xonxoff=0)
        #delete all sms except the unread ones
        modem.write("AT+CMGD=2,3\r")
        time.sleep(.5)
        #change to text mode and enable reporting
        modem.write("AT+CMGF=1\r")
        time.sleep(.5)
        modem.write("AT+CNMI=2,0,0,0,0\r")
        time.sleep(.5)
        modem.write("AT+CSMP=49,167,0,0\r")
        time.sleep(.5)
        #send sms and get reference number
        refNum = []
        sesId = uuid.uuid1()
        for n in range(0,trial):
            cmd = 'AT+CMGS="' + phoneNum + '"\r'
            msg = 'Session ' + str(sesId) + ': trial number ' + str(n)
            #print cmd
            #print msg
            modem.flushOutput()
            modem.write(cmd)
            time.sleep(.5)
            modem.write(msg)
            time.sleep(.5)
            modem.write(chr(26))
            time.sleep(.5)
            rspn = modem.read(1024)
            #print rspn
            refNumPattern = r'CMGS: (\d+)'
            num = re.findall(refNumPattern,rspn)
            refNum.append(num[0])
            time.sleep(.5)
        #wait (delay for sms to reach destination)
        time.sleep(2)
        #print refNum
        #list all sms
        modem.write('AT+CMGL="ALL"\r')
        rspn = modem.read(2048)
        #print rspn
        modem.close()
        #count the occurrence of sms ref number is on the list
        ocr = 0
        for t in refNum:
            tPattern = ',6,' + t
            #from my observation, only received sms has report
            if re.search(tPattern,rspn):
                ocr += 1
        #return occurance per trial
        return trial,ocr
        
    except:
        print "!!! get sms delivery percentage error  !!!"
        modem.close()
        sys.exit(1)
