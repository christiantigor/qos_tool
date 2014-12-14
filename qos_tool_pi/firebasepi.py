import sys,time
import MySQLdb
from firebase import firebase

db = MySQLdb.connect("localhost","monitor","password","qostool")
curs = db.cursor()

firebase = firebase.FirebaseApplication('https://radiant-torch-2376.firebaseio.com', None)

#get length of table on cloud db
try:
    table = firebase.get('/qosresult', None)
    print 'table length on cloud: %d' % len(table)
except:
    print '!!! error get length of cloud db  !!!'
    db.close()
    #sys.exit(1)

#clear table on cloud db if exceed capacity
try:
    maxrecord = 1000
    if len(table) > maxrecord:
        firebase.delete('/qosresult', None)
        firebase.put('/qosresult/0','operator', 'undefined') #dummy value so /qosresult/ can be created
    else:
        pass
    table = firebase.get('/qosresult', None) #get length of table on cloud db again
except:
    print '!!! error clear table on cloud db  !!!'
    db.close()
    #sys.exit(1)

#use local db
try:
    cmd = 'USE qostool;'
    curs.execute(cmd)
except:
    print '!!! error use local db  !!!'
    db.close()
    #sys.exit(1)

#send data from local db to cloud db
try:
    cmd = 'SELECT * FROM testresult WHERE status != "sent";'
    curs.execute(cmd)
    if len(table) == 1: #indicate the cloud db have just been cleared
        i = len(table)-2
    else:
        i = len(table)-1
    
    try:
        for data in curs.fetchall():
            i = i+1
            tab = '/qosresult/'+str(i)
            firebase.put(tab,'tddate',str(data[1]))
            firebase.put(tab,'tdtime',str(data[2]))
            firebase.put(tab,'lat',str(data[3]))
            firebase.put(tab,'lng',str(data[4]))
            firebase.put(tab,'oper',str(data[5]))
            firebase.put(tab,'bal',str(data[6]))
            firebase.put(tab,'rssi',str(data[7]))
            firebase.put(tab,'sysmode',str(data[8]))
            firebase.put(tab,'sms',str(data[10]))
            firebase.put(tab,'mos',str(data[11]))
            firebase.put(tab,'ping',str(data[12]))
            firebase.put(tab,'dload',str(data[13]))
            firebase.put(tab,'uload',str(data[14]))
            #print str(i)
            print str(data[0])+' '+str(data[1])+' '+str(data[2])+' '+str(data[3])+' '+str(data[11])+' '+str(data[12]+' '+str(data[13]))
            updatecmd = 'UPDATE testresult SET status = "sent" WHERE id = "%d";' % data[0]
            with db:
                curs.execute(updatecmd)
    except:
        print '!!! error send data to cloud  !!!'
        db.close()
        #sys.exit(1)

#    try:
#        pass
#    except:
#        print '!!! error update sentstatus on local db  !!!'
#        db.close()
#        sys.exit(1)

except:
    print '!!! error get data from local db  !!!'
    db.close()
    #sys.exit(1)
