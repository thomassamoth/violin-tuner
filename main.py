#!/usr/bin/env python
"""Violin Tuner

This program allows someone to tune a violin. It records each sound played on 
each note and tells if it's tuned or not.
This program uses Fast Fourier Transform to get the amplitude and determine the note
"""

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
import recording


def display_FFT(DATA, chosen_note):
    """Display the FFT graph"""
    figure(figsize=(12, 4))  # sets the window size
    PlayedFrequency = functions.tracerFFT(DATA, 44100, 0.1, 0.5)  # DATA,RATE,debut,DUREE
    axis([0, 1000, 0, 1])  # axes xmin,xmax,ymin,ymax

    # print in cyan
    print(
        f"\033[96m\nPlayed frequency {chosen_note} = {str(PlayedFrequency)} Hz\n\x1B[37m"
    )
    return PlayedFrequency


"""
    RECORDING
"""

# FORMAT = pyaudio.paInt16
# CHANNELS = 1  # record in mono
# RATE = 44100
# CHUNK = 8192
# RECORD_SECONDS = 2
#WAVE_OUTPUT_FILENAME = str(target_frequency) + ".wav"
#enreg.record_audio(WAVE_OUTPUT_FILENAME)
# audio = pyaudio.PyAudio()

# # Start recording
# stream = audio.open(
#     format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK
# )

# print("\n* Recording in progress ...")

# frames = []

# for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
#     data = stream.read(CHUNK)
#     frames.append(data)

# print("\n* Recording completed\n\n")

# # End recording
# stream.stop_stream()
# stream.close()
# audio.terminate()

# waveFile = wav.open(WAVE_OUTPUT_FILENAME, "wb")
# waveFile.setnchannels(CHANNELS)
# waveFile.setsampwidth(audio.get_sample_size(FORMAT))
# waveFile.setframerate(RATE)
# waveFile.writeframes(b"".join(frames))
# waveFile.close()

"""
    MAIN
"""
def main():
    chosen_note = functions.ask_note()
    functions.pause_program(3)
    target_frequency = functions.note_frequency_dict[chosen_note]
    WAVE_OUTPUT_FILENAME = str(target_frequency) + ".wav"
    recording.record_audio(WAVE_OUTPUT_FILENAME)

    print(f"Target Frequency = {target_frequency} Hz")
    functions.fast_fourier_transform(target_frequency)

    PlayedFrequency = display_FFT(functions.fast_fourier_transform(target_frequency), chosen_note)

    functions.recording_error(PlayedFrequency)

    error_message = functions.error_percentage(
        PlayedFrequency, target_frequency, chosen_note
    )

    if error_message == False:
        functions.ask_show()


if __name__ == "__main__":
    main()
