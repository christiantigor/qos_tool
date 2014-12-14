import time
import subprocess

def sendingdata (operator,ttyUsbx):
    try:
        #get parameter for wvdial
        if operator == '"XL"':
            op = 'xl'
        elif operator == '"TELKOMSEL"':
            op = 'telkomsel'
        elif operator == '"INDOSAT"':
            op = 'indosat'
        else:
            return
        #run wvdial
        cmd = "sudo wvdial " + op + " " + ttyUsbx + " &"
        subprocess.Popen([cmd], shell = True)
        time.sleep(10)
        #set default route
        subprocess.Popen(['sudo route add default ppp0'], shell = True)
        #send data to cloud
        sendtocloud = subprocess.Popen(
            ['python firebasepi.py'],
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE,
            shell = True
        )
        sendtocloud.communicate()
        time.sleep(5)
        #stop wvdial
        cmd = "sudo poff.wvdial " + op + " " + ttyUsbx
        subprocess.Popen([cmd], shell = True)
        time.sleep(10)
    except:
        print "!!! sendingdata error  !!!"
        return
