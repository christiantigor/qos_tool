#!/usr/bin/env python

import MySQLdb
import time

db = MySQLdb.connect("localhost","monitor","password","qostool")
curs = db.cursor()

cmd = 'INSERT INTO testresult VALUES (CURRENT_DATE(),NOW(),"XL",1100,None,1.868125,no)'
with db:
    curs.execute('INSERT INTO testresult VALUES (CURRENT_DATE(),NOW(),"XL","1100","None","1.868125","no")')

#with db:
    #curs.execute("""INSERT INTO testresult
        #values(CURRENT_DATE(), NOW(), '"XL"', NULL , 12.3, 2.34, 'NotSend')""")

#with db:
    #curs.execute("""INSERT INTO testresult SET
        #tddate=CURRENT_DATE(), tdtime=NOW(), operator='"XL"'""")

time.sleep(5)

cmd = "SELECT * FROM testresult"
curs.execute(cmd)

print "\nDate           Time         Operator      Balance   SMS Perc    MOS Call     Sent Status"

for reading in curs.fetchall():
    print str(reading[0]) + "     " + str(reading[1]) + "     " + \
        reading[2] + "          " + str(reading[3]) + "      " + str(reading[4]) + "       " + str(reading[5]) + "         " + str(reading[6])
