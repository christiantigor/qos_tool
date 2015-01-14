from pydub import AudioSegment

song = AudioSegment.from_wav("telkomselCalloutput.wav")

song_louder = song + 30

song_louder.export("louder.wav","wav")
