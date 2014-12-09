from gps import *
import time
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
    def stopController(self):
        self.running = False

#start not used
#gps latitude and longitude
def gpsLocation():
    #prerequisite - start gpsd
    #sudo gpsd -b /dev/ttyUSB0 -F /var/run/gpsd.sock
    try:
        gpsd = gps(mode=WATCH_ENABLE)
        while 1:
            gpsd.next()
            print "lat ", gpsd.fix.latitude
            print "lng ", gpsd.fix.longitude
            print "alt ", gpsd.fix.altitude
            time.sleep(1)
    except:
        print "!!! get gps location error  !!!"
        sys.exit(1)
#end not used

if __name__ == '__main__':
    gpsc = gpsController()
    try:
        gpsc.start()
        for _ in range(10):
            #repeat 10 times check if lat is number and not zero then data valid
            print "lat ", gpsd.fix.latitude
            print "lng ", gpsd.fix.longitude
            time.sleep(2)
        gpsc.stopController()
        gpsc.join()
    except (KeyboardInterrupt, SystemExit):
        print "!!! user cancelled  !!!"
        gpsc.stopController()
        gpsc.join()
    except:
        print "!!! error !!!"
        gpsc.stopController()
        gpsc.join()
    finally:
        gpsc.stopController()
        gpsc.join()
