# 🎻 Violin Tuner

<div align = "center">
    
[![version - v1.1.0](https://img.shields.io/badge/version-v1.1.0-4ec1ff)](https://github.com/thomassamoth/violin-tuner/releases/tag/1.1.0)    
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
1. [**PyAudio**](https://pypi.org/project/PyAudio/)  

    ```pip install pyaudio``` 

2. [**Scipy**](https://scipy.org/) 
 
    ```pip install scipy```

3. [**Matplotlib**](https://matplotlib.org/)

    ```pip install matplotlib```
4. [**Numpy**](http://numpy.org)  

    ```pip install numpy```

# List of features to add

1. Put the recording inside a function to loop it
2. Make a function to verify harmonics (if an harmonic is louder than the fundamental, just divide it and apply the error
3. Add precisions in the error message when the wrong note is selected (e.g. the note played is closer to a 'E')
4. Relaunch the program when the note is wrong (instead of stopping it directly)  

5. Reverse the program to give the note associated with the played frequency
