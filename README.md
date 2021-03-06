# 🎻 Violin Tuner

<div align = "center">
    
<a href="">[![version - v1.2.0](https://img.shields.io/badge/version-v1.2.0-4ec1ff)](https://github.com/thomassamoth/violin-tuner/releases/tag/1.2.0)</a>
<a href="">[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)</a>
<a href="">[![python](https://img.shields.io/badge/python-3.8.10-blue)](http://python.org)</a>
</div>

Project we did a few years ago to create a violin tuner, based on a Raspberry Pi.  
<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/b/b8/Raspberry_Pi_3_B%2B_%2839906370335%29.png/1280px-Raspberry_Pi_3_B%2B_%2839906370335%29.png" height="200">  
This project is inspired by the [Roadie Tuner](https://www.roadiemusic.com/) (made for guitars) and divided into 3 parts : 
1. Find the **frequency** played by the violin
2. Turn the **motor** to reach the desired frequency
3. "User **Interface**" using a RGB LED

*This part of the project can be used by itself and doesn't need the other ones*

## Dependencies

To use this program, you must install several libraries :
- [**Scipy**](https://scipy.org/)  
    ```pip install scipy```

- [**Matplotlib**](https://matplotlib.org/)  
    ```pip install matplotlib```
- [**Numpy**](http://numpy.org)  
    ```pip install numpy```
- [**Sounddevice**](https://python-sounddevice.readthedocs.io/en/0.4.4/)  
    ```pip install sounddevice```

# List of features to add

- [X] Put the recording inside a function to loop it
- [ ] Add a filtering function to prevent the harmonics from being louder than the fundamental and to be picked up
- [ ] Add precisions in the error message when the wrong note is selected (e.g. the note played is closer to a 'E')
- [ ] Relaunch the program when the note is wrong (instead of stopping it directly)  
- [ ] Reverse the program to give the note associated with the played frequency
