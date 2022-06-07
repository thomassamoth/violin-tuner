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
from scipy.signal import butter, freqz, lfilter

# import test03
from functions import *
from recording import record, timer

COLOR_WHITE = "\n\x1B[97m"
COLOR_GREEN = "\x1B[92m"
COLOR_ORANGE = "\x1B[38;2;255;185;83m"
COLOR_CYAN = "\x1B[96m"


def main():
    chosen_note = ask_note()
    pause_program(3)

    # we get the chosen note's related frequency
    target_frequency = note_frequency_dict[chosen_note]

    WAVE_OUTPUT_FILENAME = f"{str(target_frequency)}.wav"

    record(WAVE_OUTPUT_FILENAME)

    print(
        f"%sThe target frequency associated with {chosen_note} is {target_frequency} Hz%s"
        % (COLOR_CYAN, COLOR_WHITE)
    )
    # we exctract the data from the recording
    data = get_data_from_file(target_frequency)

    played_frequency = get_peaking_frequency(data, chosen_note, rate=44_100)
    # Verifies if the recording was correct
    if not recording_error(played_frequency):      
        error_message = error_percentage(played_frequency, target_frequency, chosen_note)
        if not error_message:
            ask_show()
        else:
            print("Graphics not displayed")


if __name__ == "__main__":
    main()
