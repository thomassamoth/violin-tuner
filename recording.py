import sounddevice as sd
import time
from scipy.io.wavfile import write


def timer(duration):
    while duration:
        timer = f" {duration} seconds left"
        print(timer, end=" \r")
        time.sleep(1)
        duration -= 1


def record(filename, rate=44_100, duration=3):

    print(f"Recording during {duration} s ..........")

    # start recording
    recording = sd.rec(int(duration * rate), samplerate=rate, channels=1)  # mono
    timer(duration)  # call timer function
    sd.wait()

    # write the data in filename and save it
    write(filename, rate, recording)
