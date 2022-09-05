# 🎻 Violin Tuner

![GitHub release (latest by date)](https://img.shields.io/github/v/release/thomassamoth/violin-tuner?color=4ec1ff) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![python](https://img.shields.io/badge/python-3.8.10-blue)](http://python.org)

Project we did a few years ago to create a violin tuner, based on a Raspberry Pi.  
<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/b/b8/Raspberry_Pi_3_B%2B_%2839906370335%29.png/1280px-Raspberry_Pi_3_B%2B_%2839906370335%29.png" height="200">  
The initial project was inspired by the [Roadie Tuner](https://www.roadiemusic.com/) (made for guitars) and divided into 3 parts :

1. Find the **frequency** played by the violin
2. Turn the **motor** to reach the desired frequency
3. User **Interface** using a RGB LED

> **Note**  
This part of the project can be used by itself and doesn't need the other ones.  

## Dependencies

To use this program and install packages,  simply run `pip install -r requirements.txt`

## List of features to add

- [X] Put the recording inside a function to loop it
- [X] Add more precision for a frequency to be detected
- [ ] Make a function to verify harmonics (if an harmonic is louder than the fundamental, just divide it and apply the error
- [ ] Add precisions in the error message when the wrong note is selected (e.g. the note played is closer to a 'E')
- [ ] Relaunch the program when the note is wrong (instead of stopping it directly)  
- [ ] Reverse the program to give the note associated with the played frequency
