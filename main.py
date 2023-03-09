#!/usr/bin/env python
"""Violin Tuner
This program allows someone to tune a violin. It records each sound played on 
each note and tells if it's tuned or not.
It uses Fast Fourier Transform to get the amplitude and determine the note.
"""

import argparse
import math

import scipy.io.wavfile as sciwave
from ansiconverter.converter import RGBtoANSI

from functions import *
from recording import record


def main():

    args = parser.parse_args()

    if args.string:
        chosen_note = args.string.upper()
        print(f"Using string '{chosen_note}' specified by command-line argument")

    else:
        print("No string specified with command-line.")
        chosen_note = ask_note()

    # Get the chosen note's related frequency.
    target_frequency = note_frequency_dict[chosen_note]

    # Generate the name from the frequency.
    wav_output_filename = f"{str(target_frequency)}.wav"

    pause_program(5)

    # Record the audio file.
    record(wav_output_filename, rate=44_100, duration=3)

    print(
        f"The frequency associated with {chosen_note} is {HEXtoANSI(f'{target_frequency:.2f} Hz', '#EC9706')}"
    )

    # Extract the data from the audio file.
    data = get_data_from_file(target_frequency)

    if args.precision == 0:
        precision = 1
    elif args.precision == 1:
        pass
    elif args.precision == 2:
        precision = 3

    # Get the FFT peak value and the frequency associated with it.
    played_frequency, frequence, fourier_transform = calculate_FFT(
        data, chosen_note, duree_fft=precision, rate=44_100
    )

    print(
        f"You played a note with a frequency of {RGBtoANSI(f'{played_frequency:.3f} Hz', [0, 255,247])}."
    )

    # Verify if the recording was correct.
    if not fft_error(played_frequency):  # Played frequency can't be 0 Hz.
        if not error_percentage(
            played_frequency, target_frequency, chosen_note
        ):  # Error <= ERROR_MARGIN
            ask_show(frequence, fourier_transform)  # Generate the graph & display it.

        else:
            print(RGBtoANSI("Graph not displayed", [255, 0, 0]))

    del chosen_note  # reset variable


if __name__ == "__main__":
    main()
