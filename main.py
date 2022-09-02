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

from functions import colors


def main():
    chosen_note = ask_note()

    # Gets the chosen note's related frequency.
    target_frequency = note_frequency_dict[chosen_note]

    # Generates the name from the frequency.
    WAVE_OUTPUT_FILENAME = f"{str(target_frequency)}.wav"

    pause_program(0)
    # Record the audio file.
    record(WAVE_OUTPUT_FILENAME, duration=3)

    print(
        f"%sThe frequency associated with {chosen_note} is %s{target_frequency} Hz%s"
        % (colors["COLOR_WHITE"], colors["COLOR_ORANGE"], colors["COLOR_WHITE"])
    )

    # Extract the data from the audio file.
    data = get_data_from_file(target_frequency)
        
    # Get the FFT peak value and the frequency associated with.
    played_frequency, frequence, fourier_transform = calculate_FFT(
        data,
        chosen_note,
        duree=3,
    )

    print(
        f"%sYou played a note with a frequency of {played_frequency: .3f} Hz%s"
        % (colors["COLOR_CYAN"], colors["COLOR_WHITE"])
    )

    # Verify if the recording was correct.
    if fft_error(played_frequency) is False:
        if not error_percentage(played_frequency, target_frequency, chosen_note):
            ask_show(frequence, fourier_transform)  # Generate the graph & display it.

        else:
            print("Graph not displayed\n")

    del chosen_note  # reset variable


if __name__ == "__main__":
    main()
