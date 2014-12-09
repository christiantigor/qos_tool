from gps import *
import sys, time
import threading
import math

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
            #repeat 3 times check if data is float and not nan and not zero then it's valid
            for _ in range(3):
                tLat = gpsd.fix.latitude
                tLng = gpsd.fix.longitude
                if(type(tLat) is float and not math.isnan(tLat) and type(tLng) is float and not math.isnan(tLng)):
                    if(tLat!=0.0 and tLng!=0.0):
                        #print "gps data is float and not nan and not zero"
                        lat = tLat
                        lng = tLng
                    else:
                        #print "gps data is float"
                        lat = 0.0
                        lng = 0.0
                else:
                    #print "gps data is nan"
                    lat = 0.0
                    lng = 0.0
                time.sleep(1)
            gpsc.stopController()
            gpsc.join()
            #print lat
            #print lng
            return lat, lng
        except:
            print "!!! gps get location error !!!"
            gpsc.stopController()
            gpsc.join()
            sys.exit(1)
    except:
        print "!!! gps controller error !!!"
        sys.exit(1)

#start for testing purpose
#if __name__ == '__main__':
#    latitude, longitude = gpsLocation()
#    print latitude
#    print longitude
#    time.sleep(1)
#    sys.exit(1)
#end for testing purpose
