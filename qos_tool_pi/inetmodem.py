import subprocess, sys, time

try:
    cmd = "sudo wvdial xl"
    inetmodem = subprocess.Popen(
        [cmd],
        shell = True
    )
    inetmodem.communicate()
    print "success"

    time.sleep(10)

    cmd = "ping -c 4 www.google.com"
    ping = subprocess.Popen(
        [cmd],
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE,
        shell = True
    )
    out, error = ping.communicate()
except:
    print "!!! error  !!!"
    sys.exit(1)
