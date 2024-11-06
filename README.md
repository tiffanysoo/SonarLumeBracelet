# SonarLumeBracelet
> A wearable art gadget that lights up and changes colour in response to its sound environment. 


## Table of Contents
### General-information
### Technologies Used
### Features
### Setup
### Usage- The Code
### Project Status
### Room for improvement
### Acknowledgements
### Contact



## General Information
- SonarLume Bracelet is an innovative wearable gadget.
- Coded in Python, this gadget serves as an assistive device for those with hearing impairments.
- It creates a fun and interactive experiences by responding to the sonic environment around you.
- I developed this gadget out of my love for music and concerts, as well as being inspired by a friend with a hearing impairment.
- The gadget will turn into a deeper blue the quieter the surrounding environment. 
- Conversely, the louder the environment, the more red the gadget will become.
- Spectrum of sound: deep blue_blue_cyan_teal_green_yellow-green_yellow_orange_red-orange_red


## Technologies Used
- Circuit Playground Express- version 1.0


## Features
- Changes colour based on whether sound environment is loud or quiet.
- Quiet environment will make the CPX turn blue. 
- Mid-volume environments will make the CPX turn greenish-yellow
- Loud environments will make the CPX turn red.  


## Setup
- Required to be connected to sufficient power supply- via USB or using at least X3 AAA battery pack.
- Simply connect the CPX to a sufficient power source and it will start reacting!


## Usage- Code of SonarLume Bracelet 
See below. 

# Tiffany's SonarLume Code- November 2024

# LIBRARY IMPORTS
import time
import board
import neopixel
import math as math
import audiobusio
import array

# CONSTANTS

# establishing that there are 10 neo pixels on CPX
NUM_PIXELS = 10  
pixels = neopixel.NeoPixel(board.NEOPIXEL, NUM_PIXELS, brightness=0.1, auto_write=False) #setting up board

CURVE = 2  # variable at which it records sound on logarithmic scale
SCALE_EXPONENT = math.pow(10, CURVE * -0.1)

NUM_SAMPLES = 160 #it will take 160 samples every second 

# FUNCTIONS

# Remove DC bias before computing RMS for accurate reading of sound samples recorded 
def normalized_rms(values):
    minbuf = int(mean(values))
    samples_sum = sum(
        float(sample - minbuf) * (sample - minbuf)
        for sample in values
    )

    return math.sqrt(samples_sum / len(values))
 
# defining mean to be used in removing DC bias- to help establish a consistent baseline of RMS collected
def mean(values):
    return sum(values) / len(values)

# establishing formula to calculate Decibels from sound sample. If no sound (i.e. value<=0, then DB=0)
def log10(value):
    if value <= 0:
        raise ValueError("Logarithm undefined for non-positive values.")
    return math.log(value) / math.log(10)


# Establishing logarithmic scale which sound samples are being measured to
def log_scale(input_value, input_min, input_max, output_min, output_max):
    normalized_input_value = (input_value - input_min) / \
                             (input_max - input_min)
    return output_min + \
        math.pow(normalized_input_value, SCALE_EXPONENT) \
        * (output_max - output_min)

# establishing DB formula from sound sample for cases where there is sound (i.e. rms_value >0). If no sound (i.e. rms_value=0, then DB = 0) 
def rms_to_decibels(rms_value):
    if rms_value > 0:  # To avoid taking log10 of zero or negative values
        return 20 * log10(rms_value)
    else:
        return 0


# MAIN CODE OF PROGRAM

# Set all pixels to blue
pixels.fill((0, 0, 255))  # Fill with blue
pixels.show()  # Show the colour change
print("Setting Neopixels to blue")

# Setting up MEMs Mic on CPX. Will take 16 000 samples every second- sound depth it will record up to 16) 
mic = audiobusio.PDMIn(board.MICROPHONE_CLOCK, board.MICROPHONE_DATA,
                       sample_rate=16000, bit_depth=16)

# Set up initial sample array of sound data- where NUM_SAMPLES = 160 
samples = array.array('H', [0] * NUM_SAMPLES)

# record audio data into array
mic.record(samples, len(samples))

# establishes baseline of sound- the lowest sound level where CPX neo pixels will react
input_floor = normalized_rms(samples) + 10

# Establish ceiling of sound- the highest sound level where CPX neo pixels will react
input_ceiling = input_floor + 500
# Note: could not figure out what the value of 500? Is? It is an arbitrary value that CPX understands. Unsure against what scale of measurement.

# Setting up how CPX will change colours depending on DB levels
peak = 0
while True:
    mic.record(samples, len(samples)) # will record samples forever on loop
    magnitude = normalized_rms(samples) # the recorded sampled sound level- normalized_rms(samples) is defined as simply 'magnitude')
    decibels = rms_to_decibels((magnitude)) # substitute said 'magnitude' into decibel equations 
    print(decibels) # for troubleshooting purposes- to understand what DB are read in surrounding environment 
    if decibels <= 20:
        pixels.fill((0, 0, 139))# dark blue when <= 20dB
        pixels.show()
    elif decibels <= 30:
        pixels.fill((0, 0, 255)) # blue when <= 30dB
        pixels.show()
    elif decibels <= 35:
        pixels.fill((0, 255, 255)) # cyan when <= 30dB
        pixels.show()
    elif decibels <= 40:
        pixels.fill((0, 128, 128)) #teal when <= 40 dB
        pixels.show()
    elif decibels <= 50:
        pixels.fill((0, 255, 0)) #green when <= 50 dB
        pixels.show()
    elif decibels <= 60:
        pixels.fill((173, 255, 47)) # yellow-green when <= 60 dB
        pixels.show()
    elif decibels <= 70:
        pixels.fill((255, 255, 0)) #yellow when <= 70 dB
        pixels.show()
    elif decibels <= 80:
        pixels.fill((255, 165, 0)) # orange when <= 80 dB
        pixels.show()
    elif decibels <= 90:
        pixels.fill((255, 69, 0)) # red-orange when <= 90 dB
        pixels.show()
    elif decibels <= 120:
        pixels.fill((255, 0, 0)) #red when <= 120 dB
        pixels.show()


## Project Status
Project is:  _complete/no longer_being_worked_on_because_it_is_complete.


## Room for Improvement
For future development: 
To do:
- add static feature- where a click of button can let user change between reactive colour setting and static colours.
- add pre-set colour features- similar click of button to change setting. 


## Acknowledgements
- This project was inspired by my personal love for concerts and the light-up bracelets at concert events.
- This project was based on the Playground Sound Meter developed by Dan Halbert, Tony DiCola and Kattni Remora (2017), published on Adafruit Insutries learn page. 
- Many thanks to UTS FASS teaching staff and my brother for facilitating my coding learning journey.


## Contact
Created by Tiffany Soo (Tiffany.soo@student.uts.edu.au)- feel free to contact me!



## SPDX=FileCopyrightText: 2024 Tiffany Soo
