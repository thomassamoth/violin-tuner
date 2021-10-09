# 🎻 Violin Tuner

Project we did a few years ago to create a violin tuner, based on a Raspberry Pi.  
<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/b/b8/Raspberry_Pi_3_B%2B_%2839906370335%29.png/1280px-Raspberry_Pi_3_B%2B_%2839906370335%29.png" height="200">  
This project is inspired by the [Roadie Tuner](https://www.roadiemusic.com/) (made for guitars) and divided into 3 parts : 
1. Find the **frequency** played by the violin
2. Turn the **motor** according to the received frequency to reach the wanted one
3. "User **Interface**" using an RGB LED

*This part of the project can be used by itself and doesn't need the other ones*

## Dependencies

To use this program, you must install several librairies :
1. [**PyAudio**](https://pypi.org/project/PyAudio/)  

    ```pip install pyaudio``` 

2. [**Scipy**](https://scipy.org/) 
 
    ```pip install scipy```

3. [**Matplolib**](https://matplotlib.org/)

    ```pip install matplotlib```


## Demo of the program
![gif-violon](https://user-images.githubusercontent.com/25958977/134651111-4d6e8876-c511-44a8-8cdc-d61595770aa0.gif)

Click [here](https://user-images.githubusercontent.com/25958977/134639296-85c312ac-1362-40f9-bcda-99be6f3fa52f.mp4) to see the video
