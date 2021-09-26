
#import bibliotheque
import math
import pyaudio
import numpy as np
from matplotlib.pyplot import *
import scipy.io.wavfile as sciwave
import wave as wav
from numpy.fft import fft
import os
import datetime
import time


'''choix des notes'''

note_choisie = input('\n Choisir la note : ')
# On demande à l'utilisteur de choisir la note qu'il veut accorder

note_frequence_dict = {  # on met en place un dictionnaire
    "sol": 196,
    "re": 294,
    "la": 440,
    "mi": 660
}

if note_choisie not in note_frequence_dict:
    print("Chosen note \""+note_choisie+"\" invalid")
    exit(1)

frequence_cible = note_frequence_dict[note_choisie]
# afficher la fréquence de la note  choisie
print('Fréquence cible = ', frequence_cible)
print()
# ------------------------------
'''pause dans le programme'''

pause = 3
print('Pause en cours')
time.sleep(pause)
print('fin de la pause de ', pause, 'secondes')
time.sleep(0.1)
# -----------------------------------
'''ENREGISTREMENT'''

note_choisie = str(note_choisie)


CURRENT_DATE = datetime.datetime.now()
# print(str(CURRENT_DATE))
frequence_cible = str(frequence_cible)

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 2    # secondes
WAVE_OUTPUT_FILENAME = frequence_cible + ".wav"
#WAVE_OUTPUT_FILENAME = "A_440.wav"

audio = pyaudio.PyAudio()

# Debut enregistrement
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)
print()
print("*Enregistrement en cours...")

frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print()
print("Fin d'enregistrement")


# Fin enregistrement
stream.stop_stream()
stream.close()
audio.terminate()

waveFile = wav.open(WAVE_OUTPUT_FILENAME, 'wb')
waveFile.setnchannels(CHANNELS)
waveFile.setsampwidth(audio.get_sample_size(FORMAT))
waveFile.setframerate(RATE)
waveFile.writeframes(b''.join(frames))
waveFile.close()
# -------------------------------
'''PARTIE FFT'''

# Fichier que l'on veut joindre
FILE = os.path.join(frequence_cible+".wav")
#FILE = os.path.join("440_sine.wav")


# Lecture du fichier son
RATE, DATA = sciwave.read(FILE)
TAB = np.array(DATA)
# np.set_printoptions(threshold=sys.maxsize)
# print('tab=',TAB)

n = DATA.size
DUREE = 1.0*n/RATE

# Affichage du spectre du son
te = 1.0/RATE
t = np.zeros(n)
for k in range(n):
    t[k] = te*k
figure(figsize=(12, 4))
plot(t, DATA)
xlabel("t (s)")
ylabel("amplitude")
axis([0, RECORD_SECONDS, DATA.min(), DATA.max()])
title('spectre')
grid(100)


# Calul de la transformée de Fourier
def tracerFFT(DATA, RATE, debut, DUREE):
    start = int(debut*RATE)
    stop = int((debut+DUREE)*RATE)
    spectre = np.absolute(fft(DATA[start:stop]))
    spectre = spectre/spectre.max()
    n = spectre.size

    freq = np.zeros(n)
    frequence_jouee_interne = 0
    for k in range(n):
        freq[k] = 1.0/n*RATE*k
        if spectre[k] == 1 and freq[k] < 1500:
            frequence_jouee_interne = freq[k]
    # freq, couleur fond, spectre, couleur lignes
    vlines(freq, 0, spectre, 'r')
    xlabel('f (Hz)')
    ylabel('A')
    title('Transformée de Fourier')
    axis([0, 0.5*RATE, 0, 1])
    grid()
    return [frequence_jouee_interne]


# Affichage de la FFT
figure(figsize=(12, 4))  # règle la taille des fenetres
FrequenceJouee = tracerFFT(DATA, RATE, 0.1, 0.5)  # DATA,RATE,debut,DUREE
axis([0, 1000, 0, 1])  # axes xmin,xmax,ymin,ymax
FrequenceJouee = str(FrequenceJouee)
print("\n" + 'frequence jouée', note_choisie, "=", (FrequenceJouee), "Hz")
show()  # affiche le graphique
