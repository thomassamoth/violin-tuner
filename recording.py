# Source material : https://www.techgeekbuzz.com/how-to-play-and-record-audio-in-python/

import sounddevice as sd
import time
import playsound
from scipy.io.wavfile import write


def timer(duration):
    while duration:
        mins, secs = divmod(duration, 60)
        timer = f"{mins} mins:{secs} seconds left"
        print(timer, end=" \r")
        time.sleep(1)
        duration -= 1


def record_audio(filename):

    # frequency
    rate = 44100  # frames per second
    duration = 3  # seconds in integer

    print("Recording..........")

    # start recording
    myrecording = sd.rec(int(duration * rate), samplerate=rate, channels=1)

    timer(duration)  # call timer function
    sd.wait()

    # write the data in filename and save it
    write(filename, rate, myrecording)
