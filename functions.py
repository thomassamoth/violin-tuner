#!/usr/bin/env python

import argparse
import math
import os
import time

import numpy as np
import scipy.io.wavfile as sciwave
from ansiconverter.converter import HEXtoANSI, RGBtoANSI
from matplotlib import pyplot as plt
from numpy.fft import fft

from recording import timer

# Constants
note_frequency_dict = {"G": 196.00, "D": 292.66, "A": 440.00, "E": 659.25}
ERROR_MARGIN = 20
RATE = 48_000

# Parser for the whole project.
parser = argparse.ArgumentParser(
    description="Violin Tuner",
    formatter_class=argparse.RawTextHelpFormatter,
)
parser.add_argument("-y", action="store_true", help="Display the output FFT graph.")
parser.add_argument(
    "-n", action="store_false", help="Do not display the output FFT graph (default)."
)
parser.add_argument(
    "-S",
    "--string",
    help="The string to be tuned",
    type=str.upper,
    choices=(note_frequency_dict.keys()),
)
parser.add_argument(
    "-p",
    "--precision",
    type=int,
    choices=[0, 2],
    default=2,
    help="Select the precision when calculating the Fast Fourier Transform.\n"
    "0 : fast - precise at 1 Hz\n"
    "2 : slower - precise at 1/3 Hz\n",
)

parser.add_argument("--debug", action="store_true",help="Activate the debug mode to display the audio spectrum.")

class WrongNoteChoiceError(Exception):
    """Raised when the note is not in the dictionnary."""

    pass


class FourierTransformError(Exception):
    """Raised when an error has occured during the recording"""

    pass


class ImportantPercentageError(Exception):
    """Raised when the error is over ERROR_MARGIN."""

    def warning(self):
        return "The difference is too significant. Please check if you have selected the correct string to adjust."

    def reminder(self, chosen_note):
        reminder_msg = RGBtoANSI(f"Reminder: you have chosen the note {chosen_note}\n", [255,185,83])
        return reminder_msg


def ask_note():
    """Ask the note the user wants to tune.

    Raises
        TypeError: the user entered a number and not a letter.
        WrongNoteChoiceError: the note is not in the dictionnary.

    Returns
        string: the note chosen character.
    """

    chosen_note = input("\nChoose a note to check (English naming convention) : ")
    try:
        if chosen_note.isdigit():
            raise TypeError("Please enter a letter, not a number")
            pass
        elif len(chosen_note) > 1:
            raise ValueError()

    except TypeError as e:
        print(f"{type(e)} -> {e}")
        chosen_note = ask_note()
        pass

    except ValueError as eVE:
        print(f"{type(eVE)} -> Please enter 1 letter")
        chosen_note = ask_note()
        pass

    try:
        if chosen_note.upper() not in note_frequency_dict:
            raise WrongNoteChoiceError(
                f"The note {chosen_note} is not in the dictionnary {note_frequency_dict.keys()}"
            )

    except WrongNoteChoiceError as e:
        print(f"{type(e)} -> {e}")
        chosen_note = ask_note()
        pass

    return chosen_note.upper()


def ask_show(frequence, fourier_transform):

    """Ask if the user wants to display the FFT graph.
    Graphics are separately generated if the answer is positive.
    """

    def generate_graph(frequencies, fourier_transform):
        """Generate the FFT graph"""

        plt.figure(figsize=(10, 5))  # window's height, width in inches
        plt.vlines(x=frequencies, ymin=[0], ymax=fourier_transform, colors="b")
        # frequency, background color, spectre, line colour
        # plot(frequence, 1, 'ro')
        plt.xlabel("Frequency (Hz)")
        plt.ylabel("Amplitude")
        plt.title(f"Fast Fourier Transform")
        plt.axis([0, 1000, 0, 1])
        plt.grid()
        plt.show()

    args = parser.parse_args()

    if args.n == False:
        print(RGBtoANSI("Choice '-n' : graph not displayed\n", [247, 0, 0]))
    elif args.y:
        print(HEXtoANSI("Started generating graph.... \n", "#00A67D"))
        generate_graph(frequence, fourier_transform)

    else:
        answer = None
        while answer not in ("y", "n"):
            answer = input("Do you want to display the graphics ? [y/n] ").lower()
            if answer == "y":
                print(HEXtoANSI("Started generating graph.... \n", "#00A67D"))
                generate_graph(frequence, fourier_transform)


def error_percentage(played_frequency, target_frequency, chosen_note) -> bool:
    """Calculate the error between the played frequency & the target.

    Args:
        played_frequency {float}: the picking frequency extracted from the data.
        target_frequency {float}: the frequency linked with the chosen note.
        chosen_note {string}: the note that was chosen by the user.

    Returns:
        {boolean}: An error message has been generated or not
    """

    error_message = True
    try:
        percentage_error = (
            abs(played_frequency - target_frequency) / target_frequency * 100
        )

        if percentage_error >= ERROR_MARGIN:
            raise ImportantPercentageError()

    except ImportantPercentageError as IPE:
        print(IPE.warning())
        # print(IPE.reminder(chosen_note))
        return error_message

    finally:
        print(f"Percentage Error : {percentage_error:.3f} %\n")

    if percentage_error == 0:
        print(
            RGBtoANSI(
                f"The string {chosen_note} is perfectly tuned! Well done!", [0, 255, 0]
            )
        )
        error_message = False
        return error_message


def pause_program(pause):
    """Make a pause in the program so that the user prepares to record."""

    print(f"Pause of {pause} seconds underway - Prepare for recording\n")
    timer(pause)
    # os.system("clear")


def calculate_FFT(data, chosen_note, debut=0.0, duree_fft=3.0, rate=44_100) -> float:
    """Calculate the FFT and get the peaking frequency.

    Args:
        data (numpy.ndarray): The input data
        RATE (int): Sample rate
        chosen_note (str): The note chosen by the user
        debut (float, optional): Starting point to calculate the FFT. Defaults to 0.
        duree_fft (float, optional): Duration to calculate the FFT. Defaults to 3.0.

    Returns:
        float: The frequency that has a maximum value of 1 (i.e. where there is the highest FFT value, and therefore the one which is played)
        float: The frequencies that have a FFT value.
        float: The FFT values for each frequency.
    """

    start = int(debut * RATE) # starting point for calculation of the FFT
    stop = int((debut + duree_fft) * RATE) # ending point

    fourier_transform = np.absolute(fft(data[start:stop])) # calculate the FFT for the data values.
    fourier_transform /= fourier_transform.max()  # Get a maximum value of 1 int the entire array.
    fft_size = fourier_transform.size 

    frequence = np.zeros(fft_size)  # fill a np array with zeros.
    played_frequency = 0.0  # setup a minimum value

    for i in range(int(fft_size)):
        frequence[i] = round((1.0 / fft_size) * RATE * i, 5)  # is used as the x-axis values    
        if fourier_transform[i] == np.amax(fourier_transform) and frequence[i] < 1000.0:
            played_frequency = frequence[i]

    return (
        played_frequency,
        frequence,
        fourier_transform,
    )  # needed to plot the graph afterwards


def get_data_from_file(target_frequency):
    """Extract data from the record.

    Args:
        target_frequency (float): The frequency we want to get close to.
        It is used to get the file's name as well.

    Returns:
        numpy.ndarray: The values that were extracted.
    """

    FILE = os.path.join(str(target_frequency) + ".wav")

    # Read the sound file
    RATE, data = sciwave.read(FILE)  # get the sample rate and the different values
       
    def get_data_size(data):
        """Get all the values from the array. """
        import sys
        np.set_printoptions(threshold=sys.maxsize)
        data_size = data.size
        duree_fft = 1.0 * data_size / RATE
        return data_size

    def display_sound_spectrum(data, data_size):
        """Display the audio spectrum of the recording."""
        te = 1.0 / RATE
        t = np.zeros(data_size)  # fill the array with zeros
        for k in range(data_size):
            t[k] = te * k

        plt.figure(figsize=(12, 4))
        plt.plot(t, data)
        plt.xlabel("Time (s)")
        plt.ylabel("Amplitude")
        plt.axis([0, 3, data.min(), data.max()])
        plt.title("Audio spectrum")
        plt.grid(100)
        plt.show()

    args = parser.parse_args()
    if args.debug:
        data_size = get_data_size(data)
        display_sound_spectrum(data, data_size)
    
    return data


def fft_error(PlayedFrequency) -> bool:
    """The user gets an error message if the played frequency is 0 Hz.

    Args:
        PlayedFrequency (_type_): _description_

    Raises:
        FFT: An error occured while calculating the FFT and returned freq. is 0.

    Returns:
        bool: An exception has been raised or not
    """
    try:
        if PlayedFrequency == 0:
            raise FourierTransformError(
                "An error has occured while calculating the Fourier Transform."
            )
            pass

        # os.system("clear")

    except FourierTransformError as e:
        print(f"{type(e)} -> {e}")
        print("Please try again !\n")
        return True

    return False
