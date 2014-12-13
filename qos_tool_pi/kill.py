import subprocess
import signal
import sys
import time
import qosparam

if __name__ == '__main__':
    print "test wvdial from subprocess"
    try:
        subprocess.Popen(['sudo pon.wvdial xl'], shell = True)
#        processDial.communicate()
#        time.sleep(2)
        #processDial.send_signal(signal.SIGINT)
#        processKill = subprocess.Popen(
#            ['sudo poff.wvdial xl'],
#            shell = True
#        )
        print "wvdial on"
        time.sleep(10)

        #set default route
        subprocess.Popen(['sudo route add default ppp0'], shell = True)
        time.sleep(5)

        #ping duration
        rsltPing = qosparam.pingduration('ttyUSBx')
        print "Ping: %s ms" % rsltPing

        #download and upload speed
        
        
        subprocess.Popen(['sudo poff.wvdial xl'], shell = True)
        print "wvdial off"
    except:
        print "app error"
        sys.exit(1)
