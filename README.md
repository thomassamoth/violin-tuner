# 🎻 Violin Tuner

![GitHub release (latest by date)](https://img.shields.io/github/v/release/thomassamoth/violin-tuner?color=4ec1ff&style=for-the-badge) [![Code style: black](https://img.shields.io/badge/code%20style-black-%23000?style=for-the-badge)](https://github.com/psf/black) [![python](https://img.shields.io/badge/python-3.6%2B-blue?style=for-the-badge)](http://python.org) [![License](https://img.shields.io/github/license/thomassamoth/violin-tuner?color=%234c1&style=for-the-badge)](https://github.com/thomassamoth/violin-tuner/blob/main/LICENSE)  [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=for-the-badge)](https://makeapullrequest.com)

A group project we did a few years ago to create a violin tuner, based on a Raspberry Pi.  
The initial project was inspired by the [Roadie Tuner](https://www.roadiemusic.com/) (made for guitars) and divided into 3 parts :

1. Find the **frequency** played by the violin
2. Turn the **motor** to reach the desired frequency
3. User **Interface** using a RGB LED

> **Note**  
This repository contains the first part of the whole project and it can be used by itself. It doesn't need the other parts.  

## Install  

- Clone this repository.

```bash
 git clone https://github.com/thomassamoth/violin-tuner.git
 ```

- Install all the necessary python packages.

```bash
pip install -r requirements.txt
```

## Usage

After cloning the repo, `cd` in the directory :

``` bash
cd violin-tuner 
```

You can both use the program with the ```python main.py``` command or with the [command-line interface](#cli-usage) for a quicker use.

### CLI Usage

```bash
python main.py 

usage: main.py [-h] [-y] [-n] [-S {G,D,A,E}] [-p {0,2}]

Violin Tuner

options:
  -h, --help            show this help message and exit
  -y                    Display the output FFT graph.
  -n                    Do not display the output FFT graph (default).
  -S {G,D,A,E}, --string {G,D,A,E}
                        The string to be tuned
  -p {0,2}, --precision {0,2}
                        Select the precision when calculating the Fast Fourier Transform.
                        0 : fast - precise at 1 Hz
                        2 : slower - precise at 1/3 Hz
```

## List of features to add

- [X] Group the recording code within a function to enable looping.
- [X] Add more precision when a frequency is detected.
- [ ] Filter out the high frequencies if an harmonic is detected, to prevent the latter to be detected.
- [ ] Add the closest note in the error message when the wrong note is selected.
- [ ] Relaunch the program when the note is wrong (instead of stopping it directly).
- [ ] Reverse the program to give the note associated with the played frequency.

## License  

The `Violin Tuner` program is under the **[GPL-3.0 license](http://github.com/thomassamoth/violin-tuner/blob/main/LICENSE)**.
