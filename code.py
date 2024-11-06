# Tiffany's SonarLume Code- 2.11.2024
# LIBRARY IMPORTS
import time
import board
import neopixel
import math as math
import audiobusio
import array

# CONSTANTS

NUM_PIXELS = 10  # Adjust according to your setup
pixels = neopixel.NeoPixel(board.NEOPIXEL, NUM_PIXELS, brightness=0.1, auto_write=False)

CURVE = 2
SCALE_EXPONENT = math.pow(10, CURVE * -0.1)

NUM_SAMPLES = 160

# FUNCTIONS

# Remove DC bias before computing RMS.
def normalized_rms(values):
    minbuf = int(mean(values))
    samples_sum = sum(
        float(sample - minbuf) * (sample - minbuf)
        for sample in values
    )

    return math.sqrt(samples_sum / len(values))

def mean(values):
    return sum(values) / len(values)

def log10(value):
    if value <= 0:
        raise ValueError("Logarithm undefined for non-positive values.")
    return math.log(value) / math.log(10)


def log_scale(input_value, input_min, input_max, output_min, output_max):
    normalized_input_value = (input_value - input_min) / \
                             (input_max - input_min)
    return output_min + \
        math.pow(normalized_input_value, SCALE_EXPONENT) \
        * (output_max - output_min)

def rms_to_decibels(rms_value):
    if rms_value > 0:  # To avoid taking log10 of zero or negative values
        return 20 * log10(rms_value)
    else:
        return 0



# MAIN CODE OF PROGRAM

# Set all pixels to red
pixels.fill((0, 0, 255))  # Fill with blue
pixels.show()  # Show the color change
print("Setting Neopixels to red")

# Set up mic

mic = audiobusio.PDMIn(board.MICROPHONE_CLOCK, board.MICROPHONE_DATA,
                       sample_rate=16000, bit_depth=16)

# Set up initial sample aray of sound data
samples = array.array('H', [0] * NUM_SAMPLES)

# record audio data into array
mic.record(samples, len(samples))

# establishes baseline
input_floor = normalized_rms(samples) + 10

# Establish ceiling
input_ceiling = input_floor + 500
# what is 500?? how does this change the way it reacts?

peak = 0
while True:
    mic.record(samples, len(samples))
    magnitude = normalized_rms(samples)
    decibels = rms_to_decibels((magnitude))
    print(decibels)
    if decibels <= 20:
        pixels.fill((0, 0, 139))# dark blue
        pixels.show()
    elif decibels <= 30:
        pixels.fill((0, 0, 255)) # blue
        pixels.show()
    elif decibels <= 35:
        pixels.fill((0, 255, 255)) # blue
        pixels.show()
    elif decibels <= 40:
        pixels.fill((0, 128, 128)) #cyan
        pixels.show()
    elif decibels <= 50:
        pixels.fill((0, 255, 0)) #green
        pixels.show()
    elif decibels <= 60:
        pixels.fill((173, 255, 47)) # yellow-green
        pixels.show()
    elif decibels <= 70:
        pixels.fill((255, 255, 0)) #yellow
        pixels.show()
    elif decibels <= 80:
        pixels.fill((255, 165, 0)) # orange
        pixels.show()
    elif decibels <= 90:
        pixels.fill((255, 69, 0)) # red-orange
        pixels.show()
    elif decibels <= 120:
        pixels.fill((255, 0, 0)) #red
        pixels.show()



#hello





