import pyaudio

CHUNK = 4096
CHANNELS = 1
RATE = 44100


p = pyaudio.PyAudio()

stream = p.open(format=pyaudio.paInt16,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                output=True,
                frames_per_buffer=CHUNK)

print("recording")

while 1:
    data = stream.read(CHUNK)
    stream.write(data, CHUNK)

print("end")

stream.stop_stream()
stream.close()

p.terminate()
