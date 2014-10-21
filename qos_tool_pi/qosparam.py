import re, serial, subprocess, sys, time, uuid
import simbalance
import pyaudio
import wave

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
        time.sleep(1)
        #change to text mode and enable reporting
        modem.write("AT+CMGF=1\r")
        time.sleep(1)
        modem.write("AT+CNMI=2,0,0,0,0\r")
        time.sleep(1)
        modem.write("AT+CSMP=49,167,0,0\r")
        time.sleep(1)
        #send sms and get reference number
        refNum = []
        sesId = uuid.uuid1()
        for n in range(0,trial):
            cmd = 'AT+CMGS="' + phoneNum + '"\r'
            msg = 'Session ' + str(sesId) + ': trial number ' + str(n)
            #print cmd
            #print msg
            #modem.flushOutput()
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

#get 3SQM - single sided speech quality measurement
def speechquality(ttyUsbx):
    #init
    try:
        chunk = 1024
        format = pyaudio.paInt16
        channels = 1
        rate = 8000
        dummyRate = int(2.5*rate)#in rpi, if rate is set 8000, it only record 2 sec although recordSecs is set 5
        recordSecs = 5
        waveOutName = "calloutput.wav"

        pM = "/dev/"+ttyUsbx
        pS = "/dev/ttyUSB1"#PERLU PROGRAM TAMBAHAN UNTUK MENGECEK PORT YANG MENGELUARKAN DATA
        modem = serial.Serial(port=pM,baudrate=115200,timeout=1,rtscts=0,xonxoff=0)
        stream = serial.Serial(port=pS,baudrate=115200,timeout=1,rtscts=0,xonxoff=0)
    except:
        print"!!! init speech quality error  !!!"
        modem.close()
        stream.close()
        sys.exit(1)

    #call IVR
    try:
        modem.write("ATD123;\r") #for XL number only
        time.sleep(2)
        modem.write("AT^DDSETEX=2\r")
        time.sleep(3)
        modem.close()
    except:
        print"!!! call IVR error  !!!"
        modem.close()
        stream.close()
        sys.exit(1)
        
    #record response
    try:
        #p = pyaudio.PyAudio()
        frames = []
        for i in range(0, int(dummyRate / chunk * recordSecs)):
            data = stream.read(chunk)
            #print data
            frames.append(data)
        stream.close()
    except:
        print "!!! record IVR response error  !!!"
        modem.close()
        stream.close()
        sys.exit(1)
    
    #save to file
    try:
        wf = wave.open(waveOutName, 'wb')
        wf.setnchannels(channels)
        #wf.setsampwidth(p.get_sample_size(format))
        wf.setsampwidth(2)#if uncomment the above code, must uncomment p = pyaudio.PyAudio()
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))
        wf.close()
    except:
        print "!!! save to file error  !!!"
        modem.close()
        stream.close()
        sys.exit(1)
        
    #calculate speech quality using P.536 algoritm
    try:
        cmd = "./p563 " + waveOutName
        p563 = subprocess.Popen(
            [cmd],
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE,
            shell = True
        )

        out, error = p563.communicate()

        #print out
        if out:
            try:
                mMatcher = re.compile("(\d+.\d+)")
                mos = mMatcher.findall(out)
                return mos[0]
            except:
                print "!!! regex p536 error  !!!"
        else:
            print "!!! regex no output error  !!!"
    except:
        print "!!! calculate speech quality error !!!"
        modem.close()
        stream.close()
        sys.exit(1)
