#!/usr/bin/env python

import math
import os
import time

import scipy.io.wavfile as sciwave
from matplotlib.pyplot import *
from numpy.fft import fft

# Colors for displaying text
COLOR_WHITE = "\x1B[37m"
COLOR_GREEN = "\x1B[92m"
COLOR_ORANGE = "\x1B[38;2;255;185;83m"
COLOR_CYAN = "\x1B[38;2;0;255;247m"
COLOR_RED = "\x1B[31m"
COLOR_RESET = "\x1b[0m"

note_frequency_dict = {"G": 196.00, "D": 292.66, "A": 440.00, "E": 659.25}


ERROR_MARGIN = 20  # %


class WrongNoteChoiceError(Exception):
    """Raised when the note is not in the dictionnary."""

    pass


class ImportantPercentageError(Exception):
    """Raised when the error is over ERROR_MARGIN."""

    def warning(self):
        warning_msg = """Too important difference 
            Please verify you have chosen the right string to tune """

        return f"{type(ImportantPercentageError(Exception))} -> {warning_msg}"

    def reminder(self, chosen_note):
        reminder_msg = f"%sReminder%s: you have chosen the note %s{chosen_note}%s" % (
            COLOR_ORANGE,
            COLOR_WHITE,
            COLOR_CYAN,
            COLOR_WHITE,
        )
        return reminder_msg


class FftError(Exception):
    """Raised when an error has occured during the recording"""

    pass


def ask_note():
    """Ask the note the user wants to tune.

    Raises
        TypeError: the user entered a number and not a letter
        WrongNoteChoiceError: the note is not in the dictionnary

    Returns
        string: the note that was chosen by the user
    """
    chosen_note = input("\nChoose a note to check (English naming convention) : ")
    try:
        if chosen_note.isdigit():
            raise TypeError("Please enter a letter and not a number")
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
        # chosen_note
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
    """Asks if the user wants to display the FFT graph.
    Graphics has been generated in functions.tracerFFT()
    """

    def generate_graph(frequence, fourier_transform):
        """Generate the main graph"""

        figure(figsize=(10, 5))  # window's height, width in inches
        vlines(x=frequence, ymin=[0], ymax=fourier_transform, colors="b")
        # frequency, background color, spectre, line colour
        #plot(frequence, 1, 'ro')
        xlabel("Frequency (Hz)")
        ylabel("Amplitude")
        title(f"Fast Fourier Transform")
        axis([0, 1000, 0, 1])
        grid()
        show()
    
    answer = None
    while answer not in ("y", "n"):
        answer = input("Do you want to display the graphics ? [y/n] ").lower()
        if answer == "y":
            print("%sGraph displayed\n%s" % (COLOR_ORANGE, COLOR_WHITE))
            generate_graph(frequence, fourier_transform)
    


def error_percentage(played_frequency, target_frequency, chosen_note) -> bool:
    """Tells the error between the played frequency & the target.

    Args:
        played_frequency {float}: the picking frequency extracted from the data
        target_frequency {float}: the frequency linked with the chosen note
        chosen_note {string}: the note that was chosen by the user

    Returns:
        {boolean}: An error message has been generated or not
    """
    error_msg = True
    try:
        percentage_error = (
            abs(played_frequency - target_frequency) / target_frequency * 100
        )
        if percentage_error >= ERROR_MARGIN:
            raise ImportantPercentageError()

    except ImportantPercentageError as IPE:
        print(IPE.warning())
        print(IPE.reminder(chosen_note))
        return error_msg
    finally:
        print(f"Percentage Error : {percentage_error:.3f} %")

    if percentage_error == 0:
        print("%sYour note is tuned! Well done!%s" % (COLOR_GREEN, COLOR_WHITE))
        error_msg = False
        return error_msg


def pause_program(pause):
    """Make a pause in the program so that the user prepares to record."""

    print(f"Pause of {pause} seconds underway - Prepare for recording\n")
    time.sleep(pause)


def calculate_FFT(data, chosen_note, debut=0.0, duree=1.0, RATE=44_100) -> float:
    """Calculates the FFT and get the peaking frequency

    Args:
        data (numpy array): the input data
        RATE (int): sample rate
        chosen_note (string): the note chosen by the user
        debut (float, optional): Starting point to calculate the FFT. Defaults to 0.
        duree (float, optional): Duration. Defaults to 1.0.

    Returns:
        float: The frequency that has a maximum value of 1 (i.e. where there is the highest FFT value, and therefore the one which is played)
    """

    start = int(debut * RATE)
    stop = int((debut + duree) * RATE)

    fourier_transform = np.absolute(fft(data[start:stop]))
    fourier_transform /= fourier_transform.max()  # Get a maximum value of 1
    fft_size = fourier_transform.size

    frequence = np.zeros(fft_size)  # fill a np array with zeros
    frequence_jouee_interne = 0.0  # setup a minimum value

    for i in range(int(fft_size)):
        frequence[i] = round((1.0 / fft_size) * RATE * i, 5)  # decimals
        if fourier_transform[i] == np.amax(fourier_transform) and frequence[i] < 1000.0:
            frequence_jouee_interne = frequence[i]

    return (
        frequence_jouee_interne,
        frequence,
        fourier_transform,
    )  # needed to plot the graph afterwards


def get_data_from_file(target_frequency):
    """Exctract the data from the file we recorded.

    Args:
        target_frequency (float): the frequency we want to get close to.
        It is used to get the file's name.

    Returns:
        numpy.ndarray: _description_
    """
    FILE = os.path.join(str(target_frequency) + ".wav")

    # Play the sound file
    RATE, data = sciwave.read(FILE)  # get the sample rate and the different values
    TAB = np.array(data)  # conversion into a numpy array

    def print_data(data):
        # Get all the values from the array (--debug--)
        np.set_printoptions(threshold=sys.maxsize)
        # print("tab=", TAB)
        data_size = data.size
        # print(f"Data size: {data_size}")
        DUREE = 1.0 * data_size / RATE
        print(f"Duree: {DUREE}")
        return data_size

    def sound_spectrum(data, data_size):
        # Get the sound spectrum
        te = 1.0 / RATE
        t = np.zeros(data_size)  # fill the array with zeros
        for k in range(data_size):
            t[k] = te * k
        figure(figsize=(12, 4))
        plot(t, data)
        xlabel("t (s)")
        ylabel("Amplitude")
        axis([0, 3, data.min(), data.max()])
        title("Spectre")
        grid(100)
        show()

    # Debug
    def debug(data):
        data_size = print_data(data)
        sound_spectrum(data, data_size)

    # debug(data)
    return data


def fft_error(PlayedFrequency) -> bool:
    """The user gets an error message if the played frequency is 0 Hz.

    Args:
        PlayedFrequency (_type_): _description_

    Raises:
        FftError: An error occured while calculating the FFT and returned freq. is 0.

    Returns:
        bool: An exception has been raised or not
    """
    try:
        if PlayedFrequency == 0:
            raise FftError("An error has occured while calculating the Fourier Transform.")
        # os.system("clear")

    except FftError() as e:
        print(f"{type(e)} -> {e}")
        print("Please try again !\n")
        return True

    return False
