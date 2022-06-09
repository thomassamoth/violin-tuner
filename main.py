#!/usr/bin/env python
"""
Violin Tuner
------------
This program allows someone to tune a violin. It records each sound played on 
each note and tells if it's tuned or not.
It uses Fast Fourier Transform to get the amplitude and determine the note
"""

import math
import os
import time

import matplotlib.pyplot as plt
import numpy as np
import scipy.io.wavfile as sciwave
from matplotlib.pyplot import *
from numpy.fft import fft

from functions import *
from recording import record, timer

COLOR_WHITE = "\n\x1B[97m"
COLOR_GREEN = "\x1B[92m"
COLOR_ORANGE = "\x1B[38;2;255;185;83m"
COLOR_CYAN = "\x1B[96m"


def main():
    chosen_note = ask_note()

    # Gets the chosen note's related frequency
    target_frequency = note_frequency_dict[chosen_note]

    # Generates the name from the frequency.
    WAVE_OUTPUT_FILENAME = f"{str(target_frequency)}.wav"
    
    pause_program(5)
    # Records the audio file
    record(WAVE_OUTPUT_FILENAME, duration=3)

    print(
        f"%sThe frequency associated with {chosen_note} is %s{target_frequency} Hz%s"
        % (COLOR_WHITE,COLOR_ORANGE, COLOR_WHITE)
    )

    
    # Excracts the data from the audio file
    data = get_data_from_file(target_frequency)

    # Get the FFT peaking value and the frequency associated with
    played_frequency, frequence, fourier_transform = calculate_FFT(data, chosen_note, 0.0, duree=3,)

    print(
        f"\033[96m\nPlayed frequency {chosen_note} ={played_frequency} Hz\n\x1B[37m"
    )
    # Verifies if the recording was correct
    if fft_error(played_frequency) is False:
        if not error_percentage(played_frequency, target_frequency, chosen_note):
            ask_show(frequence, fourier_transform) # generates the graph and displays it

        else:
            print("Graph not displayed")
            
    del chosen_note # reset variable

if __name__ == "__main__":
    main()
