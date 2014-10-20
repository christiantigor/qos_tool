import serial,time
import pyaudio
import wave

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 8000
DUMMY_RATE = int(2.5*RATE)#in rpi, if RATE is set 8000, it only record 2 sec although set 5
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

modem = serial.Serial(port="/dev/ttyUSB0",baudrate=115200,timeout=1,rtscts=0,xonxoff=0)
stream = serial.Serial(port="/dev/ttyUSB1",baudrate=115200,timeout=1,rtscts=0,xonxoff=0)

try:
    print "calling"

    modem.write("ATD123;\r")
    time.sleep(2)
    modem.write("AT^DDSETEX=2\r")
    time.sleep(3)
    modem.close()
except:
    print "!!! calling error  !!!"

try:
    print "recording"

    p = pyaudio.PyAudio()
    
    frames = []

    for i in range(0, int(DUMMY_RATE / CHUNK * RECORD_SECONDS)):
        #stream.flushOutput()
        data = stream.read(CHUNK)
        print data
        frames.append(data)

    stream.close()
    print "done recording"
except:
    print "!!! recording error  !!!"

try:
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    print "done converting"
except:
    print "!!! convert wave error  !!!"
