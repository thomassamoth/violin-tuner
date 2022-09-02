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

from functions import color


def main():
    chosen_note = ask_note()

    # Gets the chosen note's related frequency.
    target_frequency = note_frequency_dict[chosen_note]

    # Generates the name from the frequency.
    WAVE_OUTPUT_FILENAME = f"{str(target_frequency)}.wav"

    pause_program(5)
    # Record the audio file.
    record(WAVE_OUTPUT_FILENAME, duration=3)

    print(
        f"{color.link_primary}The frequency associated with {chosen_note} is {color.ORANGE}{target_frequency} Hz{color.RESET}")

    # Extract the data from the audio file.
    data = get_data_from_file(target_frequency)
        
    # Get the FFT peak value and the frequency associated with.
    played_frequency, frequence, fourier_transform = calculate_FFT(
        data,
        chosen_note,
        duree=3,
    )

    print(
        f"{color.INFO_LINK}You played a note with a frequency of {played_frequency: .3f} Hz{color.RESET}"
    )

    # Verify if the recording was correct.
    if not fft_error(played_frequency): # Played frequency is not 0 Hz.
        if not error_percentage(played_frequency, target_frequency, chosen_note): # Error <= ERROR_MARGIN
            ask_show(frequence, fourier_transform)  # Generate the graph & display it.

        else:
            print(f"{color.RED}Graph not displayed{color.RESET}\n")

    del chosen_note  # reset variable


if __name__ == "__main__":
    main()
