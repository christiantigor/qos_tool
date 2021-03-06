import re, requests, serial, subprocess, sys, time, uuid
from json import dumps
import simbalance
import pyaudio
import wave
from pydub import AudioSegment

#tower location from mcc-mnc-lac-cid
def towerlocation(ttyUsbx):
    try:
        p = "/dev/"+ttyUsbx
        modem = serial.Serial(port=p,baudrate=115200,timeout=5,rtscts=0,xonxoff=0)
        modem.write("AT+CIMI\r")
        rspn = modem.read(1024)
        #print rspn
        mcc = int(rspn[10]+rspn[11]+rspn[12])
        mnc = int(rspn[13]+rspn[14])
        time.sleep(1)
        #print mcc
        #print mnc
        modem.write("AT+CREG=2\r")
        time.sleep(1)
        modem.write("AT+CREG?\r")#sometimes it returns +CREG: 2,2
        rspn = modem.read(1024)
        #print rspn
        pattern = re.compile('"\w*"')
        data = pattern.findall(rspn)
        lac = data[0]
        lac = lac.replace('"','')
        cid = data[1]
        cid = cid.replace('"','')
        lac = int(lac,16)
        cid = int(cid,16)
        #print lac
        #print cid
        payload = {
            #'token': '114087104419',
            'token': '103023317794',
            'mcc': mcc,
            'mnc': mnc,
            'cells': [{'cid': cid, 'lac': lac}]
        }
        #print payload
        rspn = requests.post(url='http://ap1.unwiredlabs.com/v2/process.php',
                             data=dumps(payload),
                             headers={'content-encoding': 'application/json'})
        o = rspn.json()
        #print o
        lat = str(o[u'lat'])
        lon = str(o[u'lon'])
        modem.close()
        return lat, lon
    except:
        print "!!! get tower location error  !!!"
        modem.close()
        return "None", "None"
        #sys.exit(1)

#network operator
def operator(ttyUsbx):
    try:
        p = "/dev/"+ttyUsbx
        modem = serial.Serial(port=p,baudrate=115200,timeout=1,rtscts=0,xonxoff=0)
        modem.write("AT+COPS?\r")
        rspn = modem.read(1024)
        pattern = r'"([A-Za-z0-9_]*)"'
        operator = re.search(pattern,rspn)
        #print operator
        if operator is None:
            #start special case for xl modem
            print "operator is None"
            #list of available network
            modem.write("AT+COPS=?\r")
            rspn = modem.read(1024)
            time.sleep(1)
            if re.search('"XL"',rspn):            
                #connect to xl network
                modem.write('AT+COPS=1,0,"XL"\r')
                time.sleep(1)
                #check network operator again
                modem.write("AT+COPS?\r")
                rspn = modem.read(1024)
                pattern = r'"([A-Za-z0-9_]*)"'
                operator = re.search(pattern,rspn)
            #end special case for xl modem
        modem.close()
        return operator.group()
    except:
        #print "!!! get network operator error !!!"
        modem.close()
        return '"None"'
        #sys.exit(1)

#sim card balance
def balance(operator,ttyUsbx):
    try:
        if operator == '"XL"':
            return simbalance.xlBalance(ttyUsbx)
        elif operator == '"TELKOMSEL"':
            return simbalance.telkomselBalance(ttyUsbx)
        elif operator == '"INDOSAT"':
            return simbalance.indosatBalance(ttyUsbx)
        else:
            #print "operator unknown"
            return "None"
            #sys.exit(1)
    except:
        #print "!!! get sim card balance error  !!!"
        return "None"
        #sys.exit(1)

#get rssi
def rssi(ttyUsbx):
    try:
        p = "/dev/"+ttyUsbx
        modem = serial.Serial(port=p,baudrate=115200,timeout=0.5,rtscts=0,xonxoff=0)
        modem.write("AT+CSQ\r")
        rspn = modem.read(1024)
        pattern = r'([0-9]*),'
        out = re.findall(pattern,rspn)
        num = int(out[0])
        rssi = -113 + (2*num)
        modem.close()
        return str(rssi)
    except:
        #print "!!! get rssi error  !!!"
        modem.close()
        return "None"
        #sys.exit(1)

#get sysmode and submode
def mode(ttyUsbx):
    try:
        p = "/dev/"+ttyUsbx
        modem = serial.Serial(port=p,baudrate=115200,timeout=0.5,rtscts=0,xonxoff=0)
        modem.write("AT^SYSINFOEX\r")
        rspn = modem.read(1024)
        pattern = r'"([A-Za-z0-9_]*)"'
        out = re.findall(pattern,rspn)
        sysmode = out[0]
        submode = out[1]
        modem.close()
        return sysmode, submode
    except:
        #print "!!! get sysmode and submode error  !!!"
        modem.close()
        return "None","None"
        #sys.exit(1)

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
            time.sleep(1)
            modem.write(msg)
            time.sleep(1)
            modem.write(chr(26))
            time.sleep(1)
            rspn = modem.read(1024)
            #print rspn
            refNumPattern = r'CMGS: (\d+)'
            num = re.findall(refNumPattern,rspn)
            refNum.append(num[0])
            time.sleep(1)
        #wait (delay for sms to reach destination)
        time.sleep(10)#telkomsel need longer delay for sms delivery report
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
            #from my observation, only the received sms has a report
            if re.search(tPattern,rspn):
                ocr += 1
        #return occurance
        return ocr
        
    except:
        #print "!!! get sms delivery percentage error  !!!"
        modem.close()
        return 0 #special case for sms return 0 instead of "None"
        #sys.exit(1)

#get 3SQM - single sided speech quality measurement
def speechquality(operator,ttyUsbStream,ttyUsbx):
    #init
    try:
        chunk = 1024
        format = pyaudio.paInt16
        channels = 1
        rate = 8000
        dummyRate = int(2.5*rate)#in rpi, if rate is set 8000, it only record 2 sec although recordSecs is set 5
        recordSecs = 5
        #waveOutName = "calloutput.wav"

        pM = "/dev/"+ttyUsbx
        pS = "/dev/"+ttyUsbStream
        modem = serial.Serial(port=pM,baudrate=115200,timeout=1,rtscts=0,xonxoff=0)
        stream = serial.Serial(port=pS,baudrate=115200,timeout=1,rtscts=0,xonxoff=0)
    except:
        #print"!!! init speech quality error  !!!"
        modem.close()
        stream.close()
        #sys.exit(1)
        pass

    #call IVR
    try:
        if operator == '"XL"':
            cmd = "ATD123;\r"
            waveOutName = "xlCalloutput.wav"
        elif operator == '"TELKOMSEL"':
            cmd = "ATD888;\r"
            waveOutName = "telkomselCalloutput.wav"
        elif operator == '"INDOSAT"':
            cmd = "ATD388;\r" #im3
            waveOutName = "indosatCalloutput.wav"
        else:
            waveOutName = "elseCalloutput.wav"
        modem.write(cmd)
        time.sleep(2)
        modem.write("AT^DDSETEX=2\r")
        time.sleep(3)
        modem.close()
    except:
        #print"!!! call IVR error  !!!"
        modem.close()
        stream.close()
        pass
        #sys.exit(1)
        
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
        #print "!!! record IVR response error  !!!"
        modem.close()
        stream.close()
        pass
        #sys.exit(1)
    
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
        #print "!!! save to file error  !!!"
        modem.close()
        stream.close()
        pass
        #sys.exit(1)
    
    #increase audio file volume
    oriAudio = AudioSegment.from_wav(waveOutName)
    louderAudio = oriAudio + 30
    louderAudio.export(waveOutName,"wav")
    
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
                m = mMatcher.findall(out)
                n = round(float(m[0]),2)
                mos = str(n)
                return mos
            except:
                #print "!!! regex p563 error  !!!"
                pass
        else:
            #print "!!! regex p563 no output error  !!!"
            return "None"
    except:
        #print "!!! calculate speech quality error !!!"
        modem.close()
        stream.close()
        return "None"
        #sys.exit(1)

#get ping duration - used on internet quality (see below)
def pingduration ():
    try:
        #run ping subprocess
        try:
            host = "74.125.68.113" #this is google.com ip
            cmd = "ping -c 4 " + host
            ping = subprocess.Popen(
                [cmd],
                stdout = subprocess.PIPE,
                stderr = subprocess.PIPE,
                shell = True
            )

            out, error = ping.communicate()

            if out:
                try:
                    matcher = re.compile("rtt min/avg/max/mdev = (\d+.\d+)/(\d+.\d+)/(\d+.\d+)/(\d+.\d+)")
                    matched = matcher.findall(out)
                    avg = matched[0][1]
                    return avg
                except:
                    #print "!!! regex ping error  !!!"
                    ping.terminate()
            else:
                #print "!!! regex ping no output error  !!!"
                ping.terminate()
                return "None"
            ping.terminate()
        except:
            #print "!!! run ping subprocess error  !!!"
            ping.terminate()
            #sys.exit(1)
    except:
        #print "!!! get ping duration error  !!!"
        return "None"
        #sys.exit(1)

#get dload and uload speed - used on internet quality (see below)
def inetspeed ():
    try:
        #run inetspeed subprocess
        try:
            #cmd = "speedtest-cli"
            cmd = "python speedtest-cli-qos"
            inetspeed = subprocess.Popen(
                [cmd],
                stdout = subprocess.PIPE,
                stderr = subprocess.PIPE,
                shell = True
            )

            out, error = inetspeed.communicate()

            if out:
                try:
                    dmatcher = re.compile("Download: (\d+.\d+)")
                    umatcher = re.compile("Upload: (\d+.\d+)")
                    dload = dmatcher.findall(out)
                    uload = umatcher.findall(out)
                    download = dload[0]
                    upload = uload[0]
                    return download, upload #notes: if no inet connection speedtest-cli-qos return 0.00 and not "None"
                except:
                    print "!!! regex inetspeed error  !!!"
                    inetspeed.terminate()
            else:
                print "!!! regex inetspeed no output error !!!"
                inetspeed.terminate()

            inetspeed.terminate()
        except:
            #print "!!! run inetspeed subprocess error  !!!"
            inetspeed.terminate()
            #sys.exit(1)
    except:
        #print "!!! get inetspeed error !!!"
        return "None","None"
        #sys.exit(1)

#internet quality
def inetquality (operator,ttyUsbx):
    try:
        #get parameter for wvdial
        if operator == '"XL"':
            op = 'xl'
        elif operator == '"TELKOMSEL"':
            op = 'telkomsel'
        elif operator == '"INDOSAT"':
            op = 'indosat'
        else:
            #print "operator unknown"
            #sys.exit(1)
            return "None", "None", "None"
        #run wvdial
        cmd = "sudo wvdial " + op + " " + ttyUsbx + " &"
        subprocess.Popen([cmd], shell = True)
        time.sleep(10)
        #set default route
        subprocess.Popen(['sudo route add default ppp0'], shell = True)
        #run pingduration process
        rsltPing = pingduration()
        #print "Ping: %s ms" % rsltPing
        time.sleep(1)
        #run inetspeed process
        rsltDload, rsltUload = inetspeed()
        #print "Dload: %s Mbits/s - Uload: %s Mbits/s" % (rsltDload,rsltUload)
        #stop wvdial
        cmd = "sudo poff.wvdial " + op + " " + ttyUsbx
        subprocess.Popen([cmd], shell = True)
        time.sleep(10)
        return rsltPing, rsltDload, rsltUload
    except:
        #print "!!! get inet quality error !!!"
        #sys.exit(1)
        return "None", "None", "None"
