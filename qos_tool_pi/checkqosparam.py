import subprocess, time
import re
import sys
import qosparam
import MySQLdb
from gps import *
import threading
import math

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

def qosmain():
    listModem = []
    
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
            #print outUdevadm

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

            #get network operator - ok, can be put to db
            operator = qosparam.operator(modem.symlink)
            modem.operator = operator
            print "Operator: %s" %operator
            time.sleep(.2)

            #get sim card balance - ok, can be put to db
            balance = qosparam.balance(modem.operator,modem.symlink)
            modem.balance = balance
            print "Balance: %s" %balance
            time.sleep(.2)

            #get rssi - ok, can be put to db
            rssi = qosparam.rssi(modem.symlink)
            modem.rssi = rssi
            print "RSSI: %s dBm" %rssi
            time.sleep(.2)

            #get sysmode and submode - ok, can be put to db
            sysmode, submode = qosparam.mode(modem.symlink)
            modem.sysmode = sysmode
            modem.submode = submode
            print "Sysmode: %s Submode: %s" % (sysmode,submode)
            time.sleep(.2)

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

            #get call quality - not fully ok, indosat cannot get value and telkomsel value is 1.0
            sQuality = qosparam.speechquality(modem.operator,modem.stream,modem.symlink)
            modem.sQuality = sQuality
            print "MOS: %s" %sQuality
            time.sleep(.5)

            #get call success (do not implement yet)

            #get internet quality - ok, can be put to db
            ping, dload, uload = qosparam.inetquality(modem.operator,modem.symlink)
            modem.ping = ping
            modem.dload = dload
            modem.uload = uload
            print "Ping duration: %s ms" %ping
            print "dload: %s Mbits/s uload: %s Mbits/s" %(dload,uload)
            time.sleep(.5)

    except:
        print "!!! get qos parameter error !!!"
        #sys.exit(1)

    #put data to database
    try:
        db = MySQLdb.connect("localhost","monitor","password","qostool")
        curs = db.cursor()

        #use python context manager for automatic rollback
        latitude = "None"
        longitude = "None"

        for m in listModem:
            cmd = ('INSERT INTO testresult VALUES (NULL,CURRENT_DATE(),NOW(),"'+str(latitude)+'","'+str(longitude)+'",'+str(m.operator)+
                   ',"'+str(m.balance)+'","'+str(m.rssi)+'","'+str(m.sysmode)+'","'+str(m.submode)+'","'+str(m.smsPerc)+
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

