#!/usr/bin/env python
''' Violin Tuner

This program allows someone to tune a violin. It records each sound played on 
each note and tells if it's tuned or not.
This program uses Fast Fourier Transform to get the amplitude and determine the note

''' 

import math
import os
import time
import wave as wav

import numpy as np
import pyaudio
import scipy.io.wavfile as sciwave
from matplotlib.pyplot import *
from numpy.fft import fft

import functions


# Display the FFT
def display_FFT(DATA):
    figure(figsize=(12, 4))  # sets the window size
    PlayedFrequency = functions.tracerFFT(
        DATA, RATE, 0.1, 0.5)  # DATA,RATE,debut,DUREE
    axis([0, 1000, 0, 1])  # axes xmin,xmax,ymin,ymax

    print("\033[96m\n" + 'Played frequency ', chosen_note, "=",
          str(PlayedFrequency), "Hz\n\x1B[37m")  # print in cyan
    return PlayedFrequency


chosen_note = functions.ask_note()
pause(3)
target_frequency = functions.note_frequency_dict[chosen_note]

# FILE = os.path.join(str(target_frequency)+".wav")
# RATE, DATA = sciwave.read(FILE)  # get the sample rate
# TAB = np.array(DATA)


''' 
    RECORDING
'''

FORMAT = pyaudio.paInt16
CHANNELS = 1  # record in mono
RATE = 44100
CHUNK = 8192
RECORD_SECONDS = 2
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

print("\n* Recording completed\n\n")

# End recording
stream.stop_stream()
stream.close()
audio.terminate()

waveFile = wav.open(WAVE_OUTPUT_FILENAME, 'wb')
waveFile.setnchannels(CHANNELS)
waveFile.setsampwidth(audio.get_sample_size(FORMAT))
waveFile.setframerate(RATE)
waveFile.writeframes(b''.join(frames))
waveFile.close()

'''
    MAIN
'''

print('Target Frequency = ', target_frequency, 'Hz\n')
functions.fast_fourier_transform(target_frequency)

PlayedFrequency = display_FFT(
    functions.fast_fourier_transform(target_frequency))

functions.recording_error(PlayedFrequency)

error_message = functions.error_percentage(
    PlayedFrequency, target_frequency, chosen_note)

if(error_message == False):
    functions.ask_show()

