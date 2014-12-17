#!/usr/bin/python

import subprocess, time
import re
import sys
import qosparam
import MySQLdb
from gps import *
import threading
import math
import senddata

#classes
class mdm:
    def __init__(self, symlink, stream):
        self.symlink = symlink
        self.stream = stream #used for receiving response from IVR - speech quality measurement
        self.towerLat = None
        self.towerLon = None
        self.operator = None
        self.balance = None
        self.rssi = None
        self.sysmode = None
        self.submode = None
        self.smsPerc = None
        self.sQuality = None
        self.ping = None
        self.dload = None
        self.uload = None

gpsd = None
class gpsController(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        global gpsd
        gpsd = gps(mode=WATCH_ENABLE)
        self.running = False
    def run(self):
        self.running = True
        global gpsd
        while self.running:
            gpsd.next()
        return #need return for killing thread
    def stopController(self):
        self.running = False

#additional function
def gpsInit():
    #list all USB device
    try:
        processAllUsb = subprocess.Popen(
            ["ls /dev/ttyUSB*"],
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE,
            shell = True
        )
        listAllUsb, errorAllUsb = processAllUsb.communicate()

        try:
            lastChar = listAllUsb[len(listAllUsb)-2]
            largest = int(lastChar)
            #print largest
        except:
            print "!!! gpsInit - last char is not a number, may indicate no gps !!!"
            sys.exit(1)
    except subprocess.CalledProcessError:
        print "!!! gpsInit - list all USB error !!!"
        sys.exit(1)

    #check what ttyUSB is the gps
    try:
        base = "sudo udevadm info --query=symlink --name=ttyUSB"
        for num in range(0, largest+1):
            cmd = base + str(num)
            processUdevGps = subprocess.Popen(
                [cmd],
                stdout = subprocess.PIPE,
                stderr = subprocess.PIPE,
                shell = True
            )
            outUdevGps, errorUdevGps = processUdevGps.communicate()
            try:
                if re.search("gps",outUdevGps):
                    gpsUsb = "ttyUSB"+str(num)
                else:
                    pass
            except:
                print "!!! gpsInit - no gps detected !!!"
                sys.exit(1)
    except subprocess.CalledProcessError:
        print "!!! gpsInit - get gps ttyUSBx error !!!"
        sys.exit(1)

    #killall gpsd
    try:
        processKillallGpsd = subprocess.Popen(
            ['sudo killall gpsd'],
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE,
            shell = True
        )
        outKillallGpsd, errorKillallGpsd = processKillallGpsd.communicate()
        time.sleep(1)
    except subprocess.CalledProcessError:
        print "!!! gpsInit - killall gpsd error !!!"
        sys.exit(1)
    #activate gpsd
    try:
        #print gpsUsb
        cmd = "sudo gpsd /dev/" + gpsUsb + " -F /var/run/gpsd.sock"
        #print cmd
        proActGpsd = subprocess.Popen(
            [cmd],
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE,
            shell = True
        )
        outActGpsd, errorActGpsd = proActGpsd.communicate()
        time.sleep(1)
    except subprocess.CalledProcessError:
        print "!!! gpsInit - activate gpsd error !!!"

def validateLoc(tmpLat, tmpLng):
    if(type(tmpLat) is float and not math.isnan(tmpLat) and type(tmpLng) is float and not math.isnan(tmpLng)):
        if(tmpLat!=0.0 and tmpLng!=0.0):
            #print "gps data is float and not nan and not zero"
            lat = str(tmpLat) #convert to string
            lng = str(tmpLng) #convert to string
        else:
            #print "gps data is float"
            lat = "None"
            lng = "None"
    else:
        #print "gps data is nan"
        lat = "None"
        lng = "None"
    return lat, lng

#main function
def main(latitude,longitude):
    #listModem = []

    #list all USB device
    try:
        processAllUsb = subprocess.Popen(
            ["ls /dev/ttyUSB*"],
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE,
            shell = True
        )
    
        listAllUsb, errorAllUsb = processAllUsb.communicate()
        #print listAllUsb
    
        #get largest number of ttyUSBx
        try:
            lastChar = listAllUsb[len(listAllUsb)-2]
            largest = int(lastChar)
            #print largest
        except:
            print "!!! last char is not a number, may indicate no usb device !!!"
            sys.exit(1)
            

    except subprocess.CalledProcessError:
        print "!!! list all USB error !!!"
        sys.exit(1)

    #list USB modem and their ttyUSBx
    try:
        base = "sudo udevadm info --query=symlink --name=ttyUSB"
        for num in range(0, largest+1):
            cmd = base + str(num)
            #print cmd

            processUdevadm = subprocess.Popen(
                [cmd],
                stdout = subprocess.PIPE,
                stderr = subprocess.PIPE,
                shell = True
            )

            outUdevadm, errorUdevadm = processUdevadm.communicate()

            try:
                if re.search("gsmmodem",outUdevadm):
                    m = mdm("ttyUSB"+str(num),"ttyUSB"+str(num+1))
                    listModem.append(m)
                    #print "ttyUSB"+str(num)+" is modem"
                    #print "ttyUSB"+str(num+1)+" is stream"
                    #pass
                else:
                    #print "ttyUSB"+str(num)+" is not modem"
                    pass
            except:
                print "!!! no modem detected !!!"
                sys.exit(1)

    except subprocess.CalledProcessError:
        print "!!! get modem's ttyUSBx error !!!"
        sys.exit(1)
    
    #get qos parameter
    try:
        for modem in listModem:
            #get tower location
            #tLat, tLon = qosparam.towerlocation(modem.symlink)
            #modem.towerLat = tLat
            #modem.towerLon = tLon
            #print "Tower lat: %s Tower lon: %s" %(tLat,tLon)
            #time.sleep(1)
                        
            #get network operator
            operator = qosparam.operator(modem.symlink)
            modem.operator = operator
            print "Operator: %s" %operator
            time.sleep(1)

            #get sim card balance
            balance = qosparam.balance(modem.operator,modem.symlink)
            modem.balance = balance
            print "Balance: %s" %balance
            time.sleep(1)

            #get rssi
            rssi = qosparam.rssi(modem.symlink)
            modem.rssi = rssi
            print "RSSI: %s dBm" %rssi
            time.sleep(1)

            #get sysmode and submode
            sysmode, submode = qosparam.mode(modem.symlink)
            modem.sysmode = sysmode
            modem.submode = submode
            print "Sysmode: %s Submode: %s" % (sysmode,submode)
            time.sleep(1)

            #get internet quality
            ping, dload, uload = qosparam.inetquality(modem.operator,modem.symlink)
            modem.ping = ping
            modem.dload = dload
            modem.uload = uload
            print "Ping duration: %s ms" %ping
            print "dload: %s Mbits/s uload: %s Mbits/s" %(dload,uload)
            time.sleep(1)

            #check get internet quality success then get call and sms quality, otherwise return none
            if all(x is not None and x != "None" for x in(modem.ping, modem.dload, modem.uload)):
                #get call quality
                sQuality = qosparam.speechquality(modem.operator,modem.stream,modem.symlink)
                modem.sQuality = sQuality
                print "MOS: %s" %sQuality
                time.sleep(1)

                #get sms delivery occurence (for demo)
                phone = "+6281514797598"
                trial = 1
                ocr = qosparam.smsdelivery(phone,trial,modem.symlink)
                modem.smsPerc = ocr
                print "[%s]SMS:%d has delivery report" % (modem.operator,ocr)
                time.sleep(1)
            else:
                modem.sQuality = "None"
                modem.smsPerc = "None"

            #get sms delivery percentage
            #//OK
            #phone = "+6281514797598"
            #trial = 2
            #ocr = qosparam.smsdelivery(phone,trial,modem.symlink)
            #perc = ocr / float(trial) * 100
            #modem.smsPerc = perc
            #print "[%s]SMS:%d sent, %.2f%% has delivery report" % (operator,trial,perc)
            #//END OK

            #check get sms delivery per operator
            #if operator == '"TELKOMSEL"':
                #ocr = qosparam.smsdelivery(phone,trial,modem.symlink)
                #perc = ocr / float(trial) * 100
                #print '[%s]SMS:%d sent, %.2f%% has delivery report' % (operator,trial,perc)
    except:
        print "!!! get qos parameter error !!!"
        #sys.exit(1)

    #put data to database
    try:
        db = MySQLdb.connect("localhost","monitor","password","qostool")
        curs = db.cursor()
        
        #use python context manager for automatic rollback

        for m in listModem:
            #remove "" from operator
            m.operator = m.operator.replace('"',"")
            #put to rawtestresult
            cmd = ('INSERT INTO rawtestresult VALUES (NULL,CURRENT_DATE(),NOW(),"'+str(latitude)+'","'+str(longitude)+'","'+str(m.operator)+
                    '","'+str(m.balance)+'","'+str(m.rssi)+'","'+str(m.sysmode)+'","'+str(m.submode)+'","'+str(m.smsPerc)+
                    '","'+str(m.sQuality)+'","'+str(m.ping)+'","'+str(m.dload)+'","'+str(m.uload)+'","new"'+')'
                  )
            print cmd
            with db:
                curs.execute(cmd)

            #filter valid data
            if all(x is not None and x != "None" for x in (m.operator, m.balance, m.rssi, m.sysmode, m.submode, m.smsPerc, m.sQuality, m.ping, m.dload, m.uload)):
                cmd = ('INSERT INTO testresult VALUES (NULL,CURRENT_DATE(),NOW(),"'+str(latitude)+'","'+str(longitude)+'","'+str(m.operator)+
                       '","'+str(m.balance)+'","'+str(m.rssi)+'","'+str(m.sysmode)+'","'+str(m.submode)+'","'+str(m.smsPerc)+
                       '","'+str(m.sQuality)+'","'+str(m.ping)+'","'+str(m.dload)+'","'+str(m.uload)+'","new"'+')'
                      )
                print cmd
                with db:
                    curs.execute(cmd)
        db.close()
    except:
        print "!!! problems put data to database  !!!"
        db.close()
        sys.exit(1)

if __name__ == '__main__':
#    time.sleep(20) #sleep after booting up
    try:
        gpsInit()
    except:
        print "init app error"
        sys.exit(1)
    gpsc = gpsController()
    try:
        gpsc.start()
        while True:
            #collect data
            for _ in range(1): #how many of data collection is repeated before sent to cloud
                lat, lng = validateLoc(gpsd.fix.latitude, gpsd.fix.longitude)
                print "GPS - Loc lat: %s Loc lng: %s\r\n" %(lat,lng)
                listModem = []
                #lat = "None" #delete
                #lng = "None" #delete
                main(lat,lng)
                print "\r\n"
                time.sleep(2)
            #send data to cloud
            print "send new data to cloud"
            op = listModem[0].operator
            ttyUsb = listModem[0].symlink
            #print op,ttyUsb
            senddata.sendingdata(op,ttyUsb)
            
    except(KeyboardInterrupt, SystemExit):
        print "killing gps thread thus kill app too"
        gpsc.stopController()
        gpsc.join()
