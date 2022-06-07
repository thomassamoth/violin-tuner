#!/usr/bin/env python

import math
import os
import time

import scipy.io.wavfile as sciwave
from matplotlib.pyplot import *
from numpy.fft import fft

COLOR_WHITE = "\x1B[37m"
COLOR_GREEN = "\x1B[92m"
COLOR_ORANGE = "\x1B[38;2;255;185;83m"
COLOR_CYAN = "\x1B[38;2;0;255;247m"
COLOR = "\033[96m"
COLOR_RED = "\x1B[31m"
COLOR_RESET = "\x1b[0m"

note_frequency_dict = {"G": 196.00, "D": 292.66, "A": 440.00, "E": 659.25}


ERROR_MARGIN = 25  # %


class WrongNoteChoiceError(Exception):
    """ Raised when the note is not in the dictionnary. """

    pass


class ImportantPercentageError(Exception):
    """ Raised when the error is over ERROR_MARGIN. """

    def warning(self):
        warning_msg = """Too important difference 
            Please verify you have chosen the right string to tune """

        return f"{type(ImportantPercentageError(Exception))} -> {warning_msg}"

    def reminder(self, chosen_note):
        reminder_msg = f"%sReminder%s: you have chosen the note {chosen_note}" % (
            COLOR_ORANGE,
            COLOR_WHITE,
        )
        return reminder_msg


class RecordingError(Exception):
    """Raised when an error has occured during the recording"""

    pass


def ask_note():
    """ Ask the note the user wants to tune.

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
        chosen_note
        if chosen_note.upper() not in note_frequency_dict:
            raise WrongNoteChoiceError(
                f"The note {chosen_note} is not in the dictionnary {note_frequency_dict.keys()}"
            )

    except WrongNoteChoiceError as e:
        print(f"\t{type(e)} -> {e}")
        chosen_note = ask_note()
        pass

    return chosen_note.upper()


def ask_show():
    """Asks if the user wants to display the FFT graph.
    Graphics has been generated in functions.tracerFFT()
    """

    answer = None
    while answer not in ("y", "n"):
        answer = input("Do you want to display the graphics ? [y/n] ").lower()
        if answer == "y":
            print("%sGraph displayed\n%s" % (COLOR_ORANGE, COLOR_WHITE))
            show()


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
        print(f"Percentage Error : {percentage_error:.2f} %")

    if percentage_error == 0:
        print("%sYour note is tuned! Well done!%s" % (COLOR_GREEN, COLOR_WHITE))
        error_msg = False
        return error_msg


def pause_program(pause):
    """Make a pause in the program so that the user prepares to record."""

    print(f"Pause of {pause} seconds underway - Prepare for recording\n")
    time.sleep(pause)


def tracerFFT(data, RATE, debut=0, duree=3) -> float:
    """Calculation of the FFT.

    Args:
        data (numpy array): the input data
        RATE (integer): sample rate
        debut (integer): _description_
        duree (int, optional): _description_. Defaults to 1.

    Returns:
        float: The frequency that has a maximum value of 1 (i.e. where there is the highest FFT value, and therefore the one which is played)
    """

    start = int(debut * RATE)
    stop = int(debut + duree) * RATE

    # fourier_transform = fft(DATA[start:stop]) # Calculation of the FFT

    spectre = np.absolute(fft(data[start:stop]))
    spectre = spectre / spectre.max()  # Get a maximum value of 1
    spectre_size = spectre.size

    freq = np.zeros(spectre_size)  # fill a np array with zeros
    frequence_jouee_interne = 0

    for k in range(spectre_size):
        freq[k] = 1.0 / spectre_size * RATE * k
        if spectre[k] == 1.0 and freq[k] < 1000:
            frequence_jouee_interne = freq[k]

    # frequency, background color, spectre, line colour
    # main graph
    figure(figsize=(1920, 1080))  # window's height, width in inches
    vlines(x=freq, ymin=0, ymax=spectre, colors="b")
    xlabel("Frequency (Hz)")
    ylabel("Amplitude")
    title("Fast Fourier Transform")
    axis([0, 1000, 0, 1])
    grid()
    return frequence_jouee_interne


def get_data_from_file(target_frequency):
    """Exctract the data from the file we recorded.

    Args:
        target_frequency (float): the frequency we want to get close to.
        It is used to get the file's name.

    Returns:
        _type_: _description_
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


def recording_error(PlayedFrequency) -> bool:
    """The user gets an error message if the played frequency is 0 Hz.

    Args:
        PlayedFrequency (_type_): _description_

    Raises:
        RecordingError: An error occured while recording

    Returns:
        bool: An exception has been raised or not
    """        
    try:
        if PlayedFrequency == 0:
            raise RecordingError("An error occured while recording")
        # os.system("clear")

    except RecordingError as e:
        print(f"{type(e)} -> {e}")
        
        print("Please try again !\n")
        return True
    
    return False


def get_peaking_frequency(data, chosen_note: int, rate) -> np.float64:
    """Gets the frequency which has the highest FFT value.

    Args:
        DATA (_type_): _description_
        chosen_note (string): the note the user has chosen

    Returns:
        {numpy.float64}: frequency that is peaking 
    """

    PlayedFrequency = tracerFFT(data, rate, 0)

    print(
        f"%s\nPlayed frequency {chosen_note} : %0.2f Hz %s"
        % (COLOR_CYAN, PlayedFrequency, COLOR_WHITE)
    )
    return PlayedFrequency
