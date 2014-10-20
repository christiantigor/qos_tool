import serial
import pyaudio
import wave

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

stream = serial.Serial(port="/dev/ttyUSB1",baudrate=115200,timeout=1,rtscts=0,xonxoff=0)

print("recording")

frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    stream.flushOutput()
    data = stream.read(CHUNK)
    frames.append(data)

print("done recording")

stream.close()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(2)
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()
