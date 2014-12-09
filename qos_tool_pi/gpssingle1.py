from gps import *
import sys, time
import threading

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
        return
    def stopController(self):
        self.running = False

#gps latitude and longitude
def gpsLocation():
    #prerequisite - start gpsd
    #sudo killall gpsd
    #sudo gpsd /dev/ttyUSB0 -F /var/run/gpsd.sock
    #may need the -b flag
    try:
        gpsc = gpsController()
        try:
            gpsc.start()
            for _ in range(3):
                #repeat 3 times check if lat is number and not zero then data valid
                print "lat ", gpsd.fix.latitude
                print "lng ", gpsd.fix.longitude
                time.sleep(1)
            gpsc.stopController()
            gpsc.join()
        except:
            print "!!! gps get location error !!!"
            gpsc.stopController()
            gpsc.join()
            sys.exit(1)
    except:
        print "!!! gps controller error !!!"
        sys.exit(1)

if __name__ == '__main__':
    gpsLocation()
    time.sleep(1)
    sys.exit(1)
