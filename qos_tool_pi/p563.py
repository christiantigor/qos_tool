import subprocess,sys,time

try:
    waveOutName = "calloutput.wav"
    cmd = "./p563 " + waveOutName
    p563 = subprocess.Popen(
        [cmd],
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE,
        shell = True
    )
    out, error = p563.communicate()
    #time.sleep(30)

    print out
except:
    print "!!! error  !!!"
    sys.exit(1)
