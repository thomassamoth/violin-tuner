
import math
import os
import time
import wave as wav

import numpy as np
import pyaudio
import scipy.io.wavfile as sciwave
from matplotlib.pyplot import *
from numpy.fft import fft

note_frequency_dict = {
    "G": 196,
    "D": 294,
    "A": 440,
    "E": 660
}


def ask_note():
    chosen_note = input(
        '\nChoose a note to check (English naming convention) : ')

    if chosen_note not in note_frequency_dict:
        print("Chosen note \""+chosen_note+"\" invalid")
        chosen_note = ask_note()
        # exit(1)
    return chosen_note


chosen_note = ask_note()
target_frequency = note_frequency_dict[chosen_note]

print('Target Frequency = ', target_frequency, 'Hz\n')

# Pause in the program for the user to prepare the recording
PAUSE = 3  # seconds
print('Pause of ', PAUSE, 'seconds underway - Prepare for recording')
time.sleep(PAUSE)

time.sleep(PAUSE/10)
# -----------------------------------
'''RECORDING'''

FORMAT = pyaudio.paInt16
CHANNELS = 1  # record in mono
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 2  # seconds
WAVE_OUTPUT_FILENAME = str(target_frequency) + ".wav"

audio = pyaudio.PyAudio()

# Start recording
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

print("\n* Recording in progress ...")

frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("\n Recording completed")


# Fin enregistrement
stream.stop_stream()
stream.close()
audio.terminate()

waveFile = wav.open(WAVE_OUTPUT_FILENAME, 'wb')
waveFile.setnchannels(CHANNELS)
waveFile.setsampwidth(audio.get_sample_size(FORMAT))
waveFile.setframerate(RATE)
waveFile.writeframes(b''.join(frames))
waveFile.close()
# -------------------------------
''' Fast Fourier Transform '''

# get the file we recorded
FILE = os.path.join(str(target_frequency)+".wav")

# Play the sound file
RATE, DATA = sciwave.read(FILE)  # get the sample rate
TAB = np.array(DATA)

# To get all the values from the array (--debug--)
# np.set_printoptions(threshold=sys.maxsize)
# print('tab=',TAB)

n = DATA.size
DUREE = 1.0*n/RATE

# Get the sound spectrum
te = 1.0/RATE
t = np.zeros(n) # fill the array with zeros
for k in range(n):
    t[k] = te*k
figure(figsize=(12, 4))
plot(t, DATA)
xlabel("t (s)")
ylabel("amplitude")
axis([0, RECORD_SECONDS, DATA.min(), DATA.max()])
title('spectre')
grid(100)


# Calculation of the FFT
def tracerFFT(DATA, RATE, debut, DUREE):
    start = int(debut*RATE)
    stop = int((debut+DUREE)*RATE)
    spectre = np.absolute(fft(DATA[start:stop]))
    spectre = spectre/spectre.max()
    spectre_size = spectre.size

    freq = np.zeros(spectre_size)
    frequence_jouee_interne = 0

    for k in range(spectre_size):
        freq[k] = 1.0/spectre_size*RATE*k
        if spectre[k] == 1 and freq[k] < 1500:
            frequence_jouee_interne = freq[k]

    # frequency, background color, spectre, line colour
    vlines(freq, 0, spectre, 'r')
    xlabel('Frequency (Hz)')
    ylabel('Amplitude')
    title('Fourier Transform')
    axis([0, 0.5*RATE, 0, 1])
    grid()
    return frequence_jouee_interne


# Display the FFT
figure(figsize=(12, 4))  # sets the window size
PlayedFrequency = tracerFFT(DATA, RATE, 0.1, 0.5)  # DATA,RATE,debut,DUREE
axis([0, 1000, 0, 1])  # axes xmin,xmax,ymin,ymax
print("\033[96m\n" + 'Played frequency ', chosen_note, "=",
      str(PlayedFrequency), "Hz\n\x1B[37m")  # print in cyan

show()  # display the graph


# user get an error message if the played frequency is 0
def recording_error(PlayedFrequency):

    if PlayedFrequency == 0:
        print("\n======  ERROR =====")
        print("\x1B[37mThere's been an error while recording \033[91m")
        print("Probable cause: The microphone is too far away from the audio source")
        print("\x1B[37mPlease try again !\n")


recording_error(PlayedFrequency)
