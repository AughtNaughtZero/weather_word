# weather_word_test.py
#
# This project utilizes a 22 x 13 matrix of RGB LEDs to visualize weather forecast data pulled from an API.
#
# The Weather Word program is designed to fetch weather forecast data from an API in regular intervals, parse the data 
# into temperature, wind speed, and weather condition arrays, and then light specific sets of LEDs that represent words 
# in the 22 x 13 LED matrix.
# 
# This test program is intended to step through each word in the matrix to assist the user in general troubleshooting of
# the hardware and setup of the enclosure.
# 
# A tutorial for the complete project can be found at www.instructables.com/id/LED-Weather-Words-Forecast. The basic
# hardware and software setup can be found at https://learn.adafruit.com/neopixels-on-raspberry-pi. The NeoPixel library
# for the Raspberry Pi (rpi_ws281x library) can be found at https://github.com/jgarff. The weather data and API are provided
# by Weather Underground, LLC (WUL). An API key can be obtained at www.wunderground.com/weather/api.

import time
from neopixel import *

# LED strip configuration:
LED_COUNT      = 286                # Total number of LED pixels.
LED_PIN        = 18                 # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000             # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5                  # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255                # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False              # True to invert the signal (when using NPN transistor level shift)

def colorWipe(strip, color, wait_ms=10):
    # wipe color across display a pixel at a time
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        time.sleep(wait_ms/1000.0)
    strip.show()

def wheel(pos):
    # generate rainbow colors across 0-255 positions
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)

def rainbow(strip, wait_ms=10, iterations=1):
    # draw rainbow that fades across all pixels at once
    # iterations set to 30 which roughly corresponds to the TIME_WAIT_START constant
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i+j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)

def pixelWipe(strip, pixelData, wait_ms=10):
    # wipe pixel values across entire display one pixel at a time to display the weather words
    colors = {0:[0,0,0],1:[255,255,255]}
    for i in range(LED_COUNT):
        strip.setPixelColor(i, Color(colors[pixelData[i]][0],colors[pixelData[i]][1],colors[pixelData[i]][2]))
        time.sleep(wait_ms/1000.0)
    strip.show()

def main():
    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    print('Press Ctrl-C to quit.')

    # demonstrate LED strip with rainbow chase sequence
    rainbow(strip)

    while True:

        # light pixels for words representing 'currently'
        pixels = [0]*LED_COUNT  
        pixels[0] = 1
        pixels[1] = 1
        pixels[2] = 1
        pixels[3] = 1
        pixels[4] = 1
        pixels[5] = 1
        pixels[6] = 1
        pixels[7] = 1
        pixels[8] = 1
        pixelWipe(strip, pixels)
        time.sleep(5)
        
        # light pixels for words representing 'one'
        pixels = [0]*LED_COUNT  
        pixels[10] = 1
        pixels[11] = 1
        pixels[12] = 1
        pixelWipe(strip, pixels)
        time.sleep(5)

        # light pixels for words representing 'upcoming'
        pixels = [0]*LED_COUNT  
        pixels[18] = 1
        pixels[19] = 1
        pixels[20] = 1
        pixels[21] = 1
        pixels[22] = 1
        pixels[23] = 1
        pixels[24] = 1
        pixels[25] = 1
        pixelWipe(strip, pixels)
        time.sleep(5)

        # light pixels for words representing 'low'
        pixels = [0]*LED_COUNT  
        pixels[14] = 1
        pixels[15] = 1
        pixels[16] = 1
        pixelWipe(strip, pixels)
        time.sleep(5)

        # light pixels for words representing 'high'
        pixels = [0]*LED_COUNT  
        pixels[26] = 1
        pixels[27] = 1
        pixels[28] = 1
        pixels[29] = 1
        pixelWipe(strip, pixels)
        time.sleep(5)

        # light pixels for words representing 'minus'
        pixels = [0]*LED_COUNT  
        pixels[30] = 1
        pixels[31] = 1
        pixels[32] = 1
        pixels[33] = 1
        pixels[34] = 1
        pixelWipe(strip, pixels)
        time.sleep(5)

        # light pixels for words representing 'zero'
        pixels = [0]*LED_COUNT  
        pixels[35] = 1
        pixels[36] = 1
        pixels[37] = 1
        pixels[38] = 1
        pixelWipe(strip, pixels)
        time.sleep(5)

        # light pixels for words representing 'hundred'
        pixels = [0]*LED_COUNT  
        pixels[45] = 1
        pixels[46] = 1
        pixels[47] = 1
        pixels[48] = 1
        pixels[49] = 1
        pixels[50] = 1
        pixels[51] = 1
        pixelWipe(strip, pixels)
        time.sleep(5)

        # light pixels for words representing 'twenty'
        pixels = [0]*LED_COUNT  
        pixels[39] = 1
        pixels[40] = 1
        pixels[41] = 1
        pixels[42] = 1
        pixels[43] = 1
        pixels[44] = 1
        pixelWipe(strip, pixels)
        time.sleep(5)

        # light pixels for words representing 'twelve'
        pixels = [0]*LED_COUNT  
        pixels[52] = 1
        pixels[53] = 1
        pixels[54] = 1
        pixels[55] = 1
        pixels[56] = 1
        pixels[57] = 1
        pixelWipe(strip, pixels)
        time.sleep(5)

        # light pixels for words representing 'eleven'
        pixels = [0]*LED_COUNT  
        pixels[59] = 1
        pixels[60] = 1
        pixels[61] = 1
        pixels[62] = 1
        pixels[63] = 1
        pixels[64] = 1
        pixelWipe(strip, pixels)
        time.sleep(5)

        # light pixels for words representing 'seven'
        pixels = [0]*LED_COUNT  
        pixels[73] = 1
        pixels[74] = 1
        pixels[75] = 1
        pixels[76] = 1
        pixels[77] = 1
        pixelWipe(strip, pixels)
        time.sleep(5)

        # light pixels for words representing 'ty'
        pixels = [0]*LED_COUNT  
        pixels[71] = 1
        pixels[72] = 1
        pixelWipe(strip, pixels)
        time.sleep(5)

        # light pixels for words representing 'eigh'
        pixels = [0]*LED_COUNT  
        pixels[67] = 1
        pixels[68] = 1
        pixels[69] = 1
        pixels[70] = 1
        pixelWipe(strip, pixels)
        time.sleep(5)

        # light pixels for words representing 'ty'
        pixels = [0]*LED_COUNT  
        pixels[65] = 1
        pixels[66] = 1
        pixelWipe(strip, pixels)
        time.sleep(5)

        # light pixels for words representing 'nine'
        pixels = [0]*LED_COUNT  
        pixels[78] = 1
        pixels[79] = 1
        pixels[80] = 1
        pixels[81] = 1
        pixelWipe(strip, pixels)
        time.sleep(5)

        # light pixels for words representing 'ty'
        pixels = [0]*LED_COUNT  
        pixels[82] = 1
        pixels[83] = 1
        pixelWipe(strip, pixels)
        time.sleep(5)

        # light pixels for words representing 'thir'
        pixels = [0]*LED_COUNT  
        pixels[85] = 1
        pixels[86] = 1
        pixels[87] = 1
        pixels[88] = 1
        pixelWipe(strip, pixels)
        time.sleep(5)

        # light pixels for words representing 'ty'
        pixels = [0]*LED_COUNT  
        pixels[89] = 1
        pixels[90] = 1
        pixelWipe(strip, pixels)
        time.sleep(5)

        # light pixels for words representing 'forty'
        pixels = [0]*LED_COUNT  
        pixels[99] = 1
        pixels[100] = 1
        pixels[101] = 1
        pixels[102] = 1
        pixels[103] = 1
        pixelWipe(strip, pixels)
        time.sleep(5)

        # light pixels for words representing 'fif'
        pixels = [0]*LED_COUNT  
        pixels[96] = 1
        pixels[97] = 1
        pixels[98] = 1
        pixelWipe(strip, pixels)
        time.sleep(5)

        # light pixels for words representing 'ty'
        pixels = [0]*LED_COUNT  
        pixels[94] = 1
        pixels[95] = 1
        pixelWipe(strip, pixels)
        time.sleep(5)

        # light pixels for words representing 'one'
        pixels = [0]*LED_COUNT  
        pixels[91] = 1
        pixels[92] = 1
        pixels[93] = 1
        pixelWipe(strip, pixels)
        time.sleep(5)

        # light pixels for words representing 'six'
        pixels = [0]*LED_COUNT  
        pixels[104] = 1
        pixels[105] = 1
        pixels[106] = 1
        pixelWipe(strip, pixels)
        time.sleep(5)

        # light pixels for words representing 'ty'
        pixels = [0]*LED_COUNT  
        pixels[107] = 1
        pixels[108] = 1
        pixelWipe(strip, pixels)
        time.sleep(5)

        # light pixels for words representing 'four'
        pixels = [0]*LED_COUNT  
        pixels[109] = 1
        pixels[110] = 1
        pixels[111] = 1
        pixels[112] = 1
        pixelWipe(strip, pixels)
        time.sleep(5)

        # light pixels for words representing 'teen'
        pixels = [0]*LED_COUNT  
        pixels[113] = 1
        pixels[114] = 1
        pixels[115] = 1
        pixels[116] = 1
        pixelWipe(strip, pixels)
        time.sleep(5)

        # light pixels for words representing 'nine'
        pixels = [0]*LED_COUNT  
        pixels[126] = 1
        pixels[127] = 1
        pixels[128] = 1
        pixels[129] = 1
        pixelWipe(strip, pixels)
        time.sleep(5)

        # light pixels for words representing 'three'
        pixels = [0]*LED_COUNT  
        pixels[121] = 1
        pixels[122] = 1
        pixels[123] = 1
        pixels[124] = 1
        pixels[125] = 1
        pixelWipe(strip, pixels)
        time.sleep(5)

        # light pixels for words representing 'five'
        pixels = [0]*LED_COUNT  
        pixels[117] = 1
        pixels[118] = 1
        pixels[119] = 1
        pixels[120] = 1
        pixelWipe(strip, pixels)
        time.sleep(5)

        # light pixels for words representing 'six'
        pixels = [0]*LED_COUNT  
        pixels[130] = 1
        pixels[131] = 1
        pixels[132] = 1
        pixelWipe(strip, pixels)
        time.sleep(5)

        # light pixels for words representing 'seven'
        pixels = [0]*LED_COUNT  
        pixels[133] = 1
        pixels[134] = 1
        pixels[135] = 1
        pixels[136] = 1
        pixels[137] = 1
        pixelWipe(strip, pixels)
        time.sleep(5)

        # light pixels for words representing 'eight'
        pixels = [0]*LED_COUNT  
        pixels[138] = 1
        pixels[139] = 1
        pixels[140] = 1
        pixels[141] = 1
        pixels[142] = 1
        pixelWipe(strip, pixels)
        time.sleep(5)

        # light pixels for words representing 'two'
        pixels = [0]*LED_COUNT  
        pixels[153] = 1
        pixels[154] = 1
        pixels[155] = 1
        pixelWipe(strip, pixels)
        time.sleep(5)

        # light pixels for words representing 'ten'
        pixels = [0]*LED_COUNT  
        pixels[150] = 1
        pixels[151] = 1
        pixels[152] = 1
        pixelWipe(strip, pixels)
        time.sleep(5)

        # light pixels for words representing 'degrees'
        pixels = [0]*LED_COUNT  
        pixels[143] = 1
        pixels[144] = 1
        pixels[145] = 1
        pixels[146] = 1
        pixels[147] = 1
        pixels[148] = 1
        pixels[149] = 1
        pixelWipe(strip, pixels)
        time.sleep(5)

        # light pixels for words representing 'breezy'
        pixels = [0]*LED_COUNT  
        pixels[156] = 1
        pixels[157] = 1
        pixels[158] = 1
        pixels[159] = 1
        pixels[160] = 1
        pixels[161] = 1
        pixelWipe(strip, pixels)
        time.sleep(5)

        # light pixels for words representing 'windy'
        pixels = [0]*LED_COUNT  
        pixels[162] = 1
        pixels[163] = 1
        pixels[164] = 1
        pixels[165] = 1
        pixels[166] = 1
        pixelWipe(strip, pixels)
        time.sleep(5)

        # light pixels for words representing '&'
        pixels = [0]*LED_COUNT  
        pixels[168] = 1
        pixelWipe(strip, pixels)
        time.sleep(5)

        # light pixels for words representing 'clear'
        pixels = [0]*LED_COUNT  
        pixels[177] = 1
        pixels[178] = 1
        pixels[179] = 1
        pixels[180] = 1
        pixels[181] = 1
        pixelWipe(strip, pixels)
        time.sleep(5)

        # light pixels for words representing 'hazy'
        pixels = [0]*LED_COUNT  
        pixels[173] = 1
        pixels[174] = 1
        pixels[175] = 1
        pixels[176] = 1
        pixelWipe(strip, pixels)
        time.sleep(5)

        # light pixels for words representing 'very'
        pixels = [0]*LED_COUNT  
        pixels[169] = 1
        pixels[170] = 1
        pixels[171] = 1
        pixels[172] = 1
        pixelWipe(strip, pixels)
        time.sleep(5)

        # light pixels for words representing 'mostly'
        pixels = [0]*LED_COUNT  
        pixels[182] = 1
        pixels[183] = 1
        pixels[184] = 1
        pixels[185] = 1
        pixels[186] = 1
        pixels[187] = 1
        pixelWipe(strip, pixels)
        time.sleep(5)

        # light pixels for words representing 'partly'
        pixels = [0]*LED_COUNT  
        pixels[188] = 1
        pixels[189] = 1
        pixels[190] = 1
        pixels[191] = 1
        pixels[192] = 1
        pixels[193] = 1
        pixelWipe(strip, pixels)
        time.sleep(5)

        # light pixels for words representing 'cold'
        pixels = [0]*LED_COUNT  
        pixels[204] = 1
        pixels[205] = 1
        pixels[206] = 1
        pixels[207] = 1
        pixelWipe(strip, pixels)
        time.sleep(5)

        # light pixels for words representing 'cloudy'
        pixels = [0]*LED_COUNT  
        pixels[198] = 1
        pixels[199] = 1
        pixels[200] = 1
        pixels[201] = 1
        pixels[202] = 1
        pixels[203] = 1
        pixelWipe(strip, pixels)
        time.sleep(5)

        # light pixels for words representing 'hot'
        pixels = [0]*LED_COUNT  
        pixels[195] = 1
        pixels[196] = 1
        pixels[197] = 1
        pixelWipe(strip, pixels)
        time.sleep(5)

        # light pixels for words representing 'flurries'
        pixels = [0]*LED_COUNT  
        pixels[208] = 1
        pixels[209] = 1
        pixels[210] = 1
        pixels[211] = 1
        pixels[212] = 1
        pixels[213] = 1
        pixels[214] = 1
        pixels[215] = 1
        pixelWipe(strip, pixels)
        time.sleep(5)

        # light pixels for words representing 'foggy'
        pixels = [0]*LED_COUNT  
        pixels[216] = 1
        pixels[217] = 1
        pixels[218] = 1
        pixels[219] = 1
        pixels[220] = 1
        pixelWipe(strip, pixels)
        time.sleep(5)

        # light pixels for words representing 'blowing'
        pixels = [0]*LED_COUNT  
        pixels[227] = 1
        pixels[228] = 1
        pixels[229] = 1
        pixels[230] = 1
        pixels[231] = 1
        pixels[232] = 1
        pixels[233] = 1
        pixelWipe(strip, pixels)
        time.sleep(5)

        # light pixels for words representing 'rain'
        pixels = [0]*LED_COUNT  
        pixels[222] = 1
        pixels[223] = 1
        pixels[224] = 1
        pixels[225] = 1
        pixelWipe(strip, pixels)
        time.sleep(5)

        # light pixels for words representing 'snow'
        pixels = [0]*LED_COUNT  
        pixels[234] = 1
        pixels[235] = 1
        pixels[236] = 1
        pixels[237] = 1
        pixelWipe(strip, pixels)
        time.sleep(5)

        # light pixels for words representing 'showers'
        pixels = [0]*LED_COUNT  
        pixels[240] = 1
        pixels[241] = 1
        pixels[242] = 1
        pixels[243] = 1
        pixels[244] = 1
        pixels[245] = 1
        pixels[246] = 1
        pixelWipe(strip, pixels)
        time.sleep(5)

        # light pixels for words representing 'thunderstorms'
        pixels = [0]*LED_COUNT  
        pixels[247] = 1
        pixels[248] = 1
        pixels[249] = 1
        pixels[250] = 1
        pixels[251] = 1
        pixels[252] = 1
        pixels[253] = 1
        pixels[254] = 1
        pixels[255] = 1
        pixels[256] = 1
        pixels[257] = 1
        pixels[258] = 1
        pixels[259] = 1
        pixelWipe(strip, pixels)
        time.sleep(5)

        # light pixels for words representing 'ice'
        pixels = [0]*LED_COUNT  
        pixels[260] = 1
        pixels[261] = 1
        pixels[262] = 1
        pixelWipe(strip, pixels)
        time.sleep(5)

        # light pixels for words representing 'blizzard'
        pixels = [0]*LED_COUNT  
        pixels[265] = 1
        pixels[266] = 1
        pixels[267] = 1
        pixels[268] = 1
        pixels[269] = 1
        pixels[270] = 1
        pixels[271] = 1
        pixels[272] = 1
        pixelWipe(strip, pixels)
        time.sleep(5)

        # light pixels for words representing 'pellets'
        pixels = [0]*LED_COUNT  
        pixels[279] = 1
        pixels[280] = 1
        pixels[281] = 1
        pixels[282] = 1
        pixels[283] = 1
        pixels[284] = 1
        pixels[285] = 1
        pixelWipe(strip, pixels)
        time.sleep(5)

        # light pixels for words representing 'likely'
        pixels = [0]*LED_COUNT  
        pixels[273] = 1
        pixels[274] = 1
        pixels[275] = 1
        pixels[276] = 1
        pixels[277] = 1
        pixels[278] = 1
        pixelWipe(strip, pixels)
        time.sleep(5)
    

main()
