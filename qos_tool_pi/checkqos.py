import subprocess
import sys
import re
import checkqosparam

def main():
    try:
        #checkqosparam.qosmain() # for testing
        processQos = subprocess.Popen(
            ['ps -ef | grep qos.py'],
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE,
            shell = True
        )
        outQos, errorQos = processQos.communicate()
        
        if outQos:
            try:
                processName = "python qos.py" #for demo
                #processName = "python checkqos.py" #for testing of what cmd that couldn't be run using cron
                if re.search(processName, outQos):
                    print "process is running"
                    return
                else:
                    print "process is not running"
                    print "run process"
                    subprocess.Popen(['python qos.py'], shell = True) #for demo
            except:
                print "!!! regex error !!!"
                return
        else:
            print "no output"
            return
    except:
        print "!!! checkqos error  !!!"
        sys.exit(1)

if __name__ == '__main__':
    main()
