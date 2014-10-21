import subprocess
import re
import sys
import qosparam

#classes
class mdm:
    def __init__(self, symlink):
        self.symlink = symlink

def main():
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
            print "!!! last char is not a number - may indicate there is no usb device !!!"
            sys.exit(1)
            

    except subprocess.CalledProcessError:
        print "!!! list all USB error !!!"
        sys.exit(1)

    #list USB modem and their ttyUSBx
    try:
        base = "udevadm info --query=symlink --name=ttyUSB"
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
                    m = mdm("ttyUSB"+str(num))
                    listModem.append(m)
                    #print "ttyUSB"+str(num)+" is modem"
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

    try:
        for modem in listModem:
            #get network operator
            operator = qosparam.operator(modem.symlink)
            print "Operator: %s" %operator

            #get sim card balance
            balance =  qosparam.balance(operator,modem.symlink)
            print "Balance: %s" %balance

            #get sms delivery percentage
            phone = "+6281514797598"
            trial,suc = qosparam.smsdelivery(phone,2,modem.symlink)
            perc = suc / float(trial) * 100
            print "SMS:%d sent, %.2f%% received" % (trial,perc)
            
            #get call success

            #get call quality
            sQuality = qosparam.speechquality(modem.symlink)
            print "Voice MOS: %s" %sQuality
    except:
        print "!!! problems in get parameter !!!"
        sys.exit(1)

if __name__ == '__main__':
    main()
