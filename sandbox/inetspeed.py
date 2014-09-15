import subprocess
import re

try:
    speedtest = subprocess.Popen(
        ["speedtest-cli"],
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE
    )

    out, error = speedtest.communicate()
    #print out

    if out:
        try:
            dmatcher = re.compile("Download: (\d+.\d+) (.+)")
            umatcher = re.compile("Upload: (\d+.\d+) (.+)")
            download = dmatcher.findall(out)
            upload = umatcher.findall(out)
            print download, upload
        except:
            print "!!! regex error !!!"
    else:
        print "!!! no output !!!"

except subprocess.CalledProcessError:
    print "!!! speedtest-cli error !!!"
