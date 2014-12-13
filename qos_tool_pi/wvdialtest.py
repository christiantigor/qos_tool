import subprocess
import signal
import sys
import time
import qosparam

if __name__ == '__main__':
    print "test wvdial from subprocess"
    try:
        subprocess.Popen(['sudo wvdial &'], shell = True)
        time.sleep(10)
#        processDial.communicate()
#        time.sleep(2)
        #processDial.send_signal(signal.SIGINT)
#        processKill = subprocess.Popen(
#            ['sudo poff.wvdial xl'],
#            shell = True
#        )
        print "wvdial on"

        #set default route
        subprocess.Popen(['sudo route add default ppp0'], shell = True)

        #ping duration
        rsltPing = qosparam.pingduration('ttyUSBx')
        print "Ping: %s ms" % rsltPing
        time.sleep(10)

        #download and upload speed
        #duload = subprocess.Popen(
        #    ['python speedtest-cli-qos'],
        #    stdout = subprocess.PIPE,
        #    stderr = subprocess.PIPE,
        #    shell = True
        #)
        #out, error = duload.communicate()
        #print out
        rsltDload, rsltUload = qosparam.inetspeed('ttyUSBx')
        print "Dload: %s Mbits/s - Uload: %s Mbits/s" % (rsltDload,rsltUload)
        
        subprocess.Popen(['sudo poff.wvdial xl'], shell = True)
        time.sleep(10)
        print "wvdial off"
    except:
        print "app error"
        sys.exit(1)
