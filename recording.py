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
    """Record the audio

    Args:
        filename (string): output name for the audio file
        rate (sample rate, optional): _description_. Defaults to 44_100.
        duration (int, optional): _description_. Defaults to 3.
    """

    print(f"Recording during {duration} seconds ..........")

    # start recording
    recording = sd.rec(int(duration * rate), samplerate=rate, channels=1)  # mono
    timer(duration)  # call timer function
    sd.wait()

    # write the data in filename and save it
    write(filename, rate, recording)
