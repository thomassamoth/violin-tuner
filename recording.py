import sounddevice as sd
import time
from scipy.io.wavfile import write


def timer(duration):
    while duration:
        timer = f" {duration} seconds left"
        print(timer, end=" \r")
        time.sleep(1)
        duration -= 1


def record(filename):

    # frequency
    rate = 44100  # frames per second
    duration = 3  # seconds

    print("Recording ..........")

    # start recording
    recording = sd.rec(int(duration * rate), samplerate=rate, channels=1)  # mono
    timer(duration)  # call timer function
    sd.wait()

    # write the data in filename and save it
    write(filename, rate, recording)
