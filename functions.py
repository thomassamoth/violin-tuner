#!/usr/bin/env python

import math
import os
import time
import wave as wav
import numpy as np
import pyaudio
import scipy.io.wavfile as sciwave
from matplotlib.pyplot import *
from numpy.fft import fft


note_frequency_dict = {
    "G": 196,
    "D": 294,
    "A": 440,
    "E": 660
}


def ask_note():
    """ Ask the user the string to be tuned """

    chosen_note = input(
        '\nChoose a note to check (English naming convention) : ').upper()

    if chosen_note not in note_frequency_dict:
        print(f"Invalid choice for the note {chosen_note}")
        chosen_note = ask_note()
        # exit(1)
    return chosen_note


def ask_show():
    """ Choice to display the graphs after recording """

    answer = input("Do you want to plot the graphs ? (y/n) ").lower()
    if answer == 'y':
        print("\x1B[38;2;255;185;83mGraph displayed\n")  # orange
        show()

    elif answer == 'n':
        print("Graph is not displayed\n")

    else:
        print("Invalid! Please, try again")
        ask_show()


def error_percentage(PlayedFrequency, target_frequency, chosen_note):
    """
    Tell the user the error there is between the played frequency and the wanted one
    """
    error_msg = False

    percentage = abs(PlayedFrequency-target_frequency)/target_frequency*100
    print(f"Percentage Error : {percentage:.2f} %")
    if percentage == 0:
        print("\x1B[32mYour note is tuned ! Well done ! \n\x1B[37m")

    elif percentage >= 20:  # 20% error margin
        print('''
            === ERROR ===
    The difference seems to be too important !
    Please verify you have chosen the right string to tune            
        ''')
        print(
            f"Reminder : you've chosen the note\x1B[38;2;0;255;247m {chosen_note}\n\x1B[37m")
        error_msg = True
        quit
    return error_msg


def pause_program(pause):
    """ Make a pause in the program so that the user prepares to record """

    print(f'Pause of {pause} seconds underway - Prepare for recording\n')
    time.sleep(pause)


def tracerFFT(DATA, RATE, debut, DUREE):
    """ Calculation of the FFT """

    start = int(debut*RATE)
    stop = int((debut+DUREE)*RATE)
    spectre = np.absolute(fft(DATA[start:stop]))
    spectre = spectre/spectre.max()
    spectre_size = spectre.size

    freq = np.zeros(spectre_size)
    frequence_jouee_interne = 0

    for k in range(spectre_size):
        freq[k] = 1.0/spectre_size*RATE*k
        if spectre[k] == 1 and freq[k] < 1500:
            frequence_jouee_interne = freq[k]

    # frequency, background color, spectre, line colour
    vlines(freq, 0, spectre, 'r')
    xlabel('Frequency (Hz)')
    ylabel('Amplitude')
    title(' Fast Fourier Transform')
    axis([0, 0.5*RATE, 0, 1])
    grid()
    return frequence_jouee_interne


def fast_fourier_transform(target_frequency):
    """ Get the file we recorded """

    FILE = os.path.join(str(target_frequency)+".wav")

    # Play the sound file
    RATE, DATA = sciwave.read(FILE)  # get the sample rate
    TAB = np.array(DATA)

    # To get all the values from the array (--debug--)
    # np.set_printoptions(threshold=sys.maxsize)
    # print('tab=',TAB)

    n = DATA.size
    DUREE = 1.0*n/RATE

    # #Get the sound spectrum
    # te = 1.0/RATE
    # t = np.zeros(n)  # fill the array with zeros
    # for k in range(n):
    #     t[k] = te*k
    # figure(figsize=(12, 4))
    # plot(t, DATA)
    # xlabel("t (s)")
    # ylabel("amplitude")
    # axis([0, RECORD_SECONDS, DATA.min(), DATA.max()])
    # title('spectre')
    # grid(100)
    return DATA


def recording_error(PlayedFrequency):
    """ The user gets an error message if the played frequency is 0 Hz """

    if PlayedFrequency == 0:
        print('''
              \n======  ERROR =====
              \x1B[37mThere's been an error while recording \033[91m
              ''')
        print(
            "\x1B1Probable cause:\x1B[0m The microphone is too far away from the audio source")
        print("\x1B[37mPlease try again !\n")
