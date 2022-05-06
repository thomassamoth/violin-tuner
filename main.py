#!/usr/bin/env python
"""Violin Tuner
This program allows someone to tune a violin. It records each sound played on 
each note and tells if it's tuned or not.
This program uses Fast Fourier Transform to get the amplitude and determine the note
"""

import math
import os
import time
import scipy.io.wavfile as sciwave
from matplotlib.pyplot import *
from numpy.fft import fft

import functions
import recording


def display_FFT(DATA, chosen_note):
    """Display the FFT graph"""
    figure(figsize=(12, 4))  # sets the window size
    PlayedFrequency = functions.tracerFFT(
        DATA, 44100, 0.1, 0.5
    )  # DATA,RATE,debut,DUREE
    axis([0, 1000, 0, 1])  # axes xmin,xmax,ymin,ymax

    # print in cyan
    print(
        f"\033[96m\nPlayed frequency {chosen_note} = {str(PlayedFrequency)} Hz\n\x1B[37m"
    )
    return PlayedFrequency


def main():
    chosen_note = functions.ask_note()
    functions.pause_program(3)
    target_frequency = functions.note_frequency_dict[chosen_note]
    WAVE_OUTPUT_FILENAME = str(target_frequency) + ".wav"

    recording.record(WAVE_OUTPUT_FILENAME)

    print(f"Target Frequency = {target_frequency} Hz")
    functions.fast_fourier_transform(target_frequency)

    PlayedFrequency = display_FFT(
        functions.fast_fourier_transform(target_frequency), chosen_note
    )

    functions.recording_error(PlayedFrequency)

    error_message = functions.error_percentage(
        PlayedFrequency, target_frequency, chosen_note
    )

    if error_message == False:
        functions.ask_show()


if __name__ == "__main__":
    main()
