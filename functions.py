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


# Ask the user the note to tune
def ask_note():
    chosen_note = input(
        '\nChoose a note to check (English naming convention) : ')

    if chosen_note not in note_frequency_dict:
        print("Chosen note \""+chosen_note+"\" invalid")
        chosen_note = ask_note()
        # exit(1)
    return chosen_note


# Choice to display the graphs
def ask_show():
    answer = input("Do you want to plot the graphs ? (y/n) ")
    if answer == 'y':
        print("\x1B[38;2;255;185;83mGraph displayed\n")  # orange
        show()

    elif answer == 'n':
        print("Graph is not displayed\n")

    else:
        print("Wrong choice, try again")
        ask_show()

# Tells the user the error there is between the played frequency and the wanted one
def error_percentage(PlayedFrequency, target_frequency, chosen_note):
    percentage = abs(PlayedFrequency-target_frequency)/target_frequency*100
    print("Percentage Error : ", "%.2f" % percentage, "%")
    if percentage == 0:
        print("\x1B[32mYour note is tuned ! Well done ! \n\x1B[37m")

    elif percentage >= 20:
        print("\n\t=== ERROR ===")
        print("The difference seems to be too important !")
        print("Please verify you have chosen the right string to tune")
        print(
            "Reminder :  you've chosen the note : \x1B[38;2;0;255;247m", chosen_note, "\n\x1B[37m")
        quit

# Make a pause in the program so that the user prepares the recording
def pause(pause):
    print('Pause of ', pause, 'seconds underway - Prepare for recording')
    time.sleep(pause)


#Calculation of the FFT
def tracerFFT(DATA, RATE, debut, DUREE):
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
    title('Fourier Transform')
    axis([0, 0.5*RATE, 0, 1])
    grid()
    return frequence_jouee_interne

def fast_fourier_transform(target_frequency):
    # get the file we recorded
    FILE = os.path.join(str(target_frequency)+".wav")

    # Play the sound file
    RATE, DATA = sciwave.read(FILE)  # get the sample rate
    TAB = np.array(DATA)

    # To get all the values from the array (--debug--)
    # np.set_printoptions(threshold=sys.maxsize)
    # print('tab=',TAB)

    n = DATA.size
    DUREE = 1.0*n/RATE

    # Get the sound spectrum
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











# user get an error message if the played frequency is 0
def recording_error(PlayedFrequency):

    if PlayedFrequency == 0:
        print("\n======  ERROR =====")
        print("\x1B[37mThere's been an error while recording \033[91m")
        print(
            "\e[1mProbable cause:\e[0m The microphone is too far away from the audio source")
        print("\x1B[37mPlease try again !\n")
