# weather_word.py
#
# This project utilizes a 22 x 13 matrix of RGB LEDs to visualize weather forecast data pulled from an API.
#
# The Weather Word program is designed to fetch weather forecast data from an API in regular intervals, parse the data 
# into temperature, wind speed, and weather condition arrays, and then light specific sets of LEDs that represent words 
# in the 22 x 13 LED matrix. The program will also generate the file log.txt which is used for general 
# troubleshooting and data review. The file is re-written at each API call.
# 
# The apiboot.txt and weather_word.py files are intended to reside at /home/pi/weather_word directory and to be launched at 
# startup by editing crontab with the instruction @reboot sudo python3 /home/pi/weather_word/weather_word.py.
# 
# A tutorial for the complete project can be found at www.instructables.com/id/LED-Weather-Words-Forecast. The basic
# hardware and software setup can be found at https://learn.adafruit.com/neopixels-on-raspberry-pi. The NeoPixel library
# for the Raspberry Pi (rpi_ws281x library) can be found at https://github.com/jgarff. The weather data and API are provided
# by Weather Underground, LLC (WUL). An API key can be obtained at www.wunderground.com/weather/api.

import time
import json
from urllib.request import urlopen
from neopixel import *

# LED strip configuration:
LED_COUNT      = 286                # Total number of LED pixels.
LED_PIN        = 18                 # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000             # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5                  # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255                # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False              # True to invert the signal (when using NPN transistor level shift)

# other constants
PATH_NAME = "//home//pi//weather_word//"  # set path to find apiboot.txt and log.txt files
TIME_BETWEEN_CALLS = 900            # time in seconds between calls to the weather api
TIME_BETWEEN_FAILED = 180           # time in seconds between failed calls to the weather api
TIME_WAIT_STARTUP = 60              # time in seconds to wait after bootup to make first call
OBJMAX = 13                         # set max number of objects to parse from weather data

def readApiBootFile(strip):
    # opens apiboot.txt file and reads the api key (obtain from weather underground) and one uncommented query line
    # this function ignores the '#' in the file for comments
    # this function will utilize a red color wipe across the LED matrix if the file fails to read
    i = 0
    a = [None]*2
    try:
        textFile = open(PATH_NAME + "apiboot.txt", "r")
        while i < 2:
            a[i] = textFile.readline().rstrip('\n')
            if a[i][0] != "#":
                i += 1
    except:
        textFile.close()
        writeLogFile("\n\n-----Error-----\n\nFailed to read apiboot.txt file.\nCheck that file exists.\nCheck that the file contains your API key.\nCheck that the file has at least one query line uncommented.", "a")
        colorWipe(strip, Color(0,255,0))
        raise SystemExit('failed to read apiboot file')
    else:
        textFile.close()
        return a

def writeLogFile(text, mode):
    # writes information to log.txt file
    textFile = open(PATH_NAME + "log.txt", mode)
    textFile.write(text)
    textFile.close()

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

def rainbow(strip, wait_ms=10, iterations=17):
    # draw rainbow that fades across all pixels at once
    # iterations set to 30 which roughly corresponds to the TIME_WAIT_START constant
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i+j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)

def parseWeatherData(strip, obj):
    # parse data obtained from the weather api
    # this function will utilize a red color wipe across the LED matrix if no data is returned from the API
    temp = [None]*OBJMAX                # array to hold temperature values
    humid = [None]*OBJMAX               # array to hold humidity values
    wind = [None]*OBJMAX                # array to hold wind speed values
    fct = [None]*OBJMAX                 # array to hold coded weather condition values
    fcttime = [None]*OBJMAX             # array to hold time of forecast
    error = 'foo'
    try:
        error = str(obj["response"]["error"]["type"])
    except:
        for i in range(OBJMAX):
            temp[i] = str(obj["hourly_forecast"][i]["temp"]["english"])
            humid[i] = str(obj["hourly_forecast"][i]["humidity"])
            wind[i] = str(obj["hourly_forecast"][i]["wspd"]["english"])
            fct[i] = str(obj["hourly_forecast"][i]["fctcode"])
            fcttime[i] = str(obj["hourly_forecast"][i]["FCTTIME"]["civil"])
        return temp, humid, wind, fct, fcttime
    else:
        writeLogFile('\n\n-----Error-----\n\n' + error,'a')
        colorWipe(strip, Color(0,255,0))
        raise SystemExit('some error from api')

def pixelAssign(temp, humid, wind, fct):
    # assign pixel values to weather data
    current = [0]*LED_COUNT          # array to hold current forecast pixel words
    upcomingMin = [0]*LED_COUNT      # array to hold low value forecast pixel words
    upcomingMax = [0]*LED_COUNT      # array to hold high value forecast pixel words
    
    # for current weather conditions
    # light pixels for words representing 'currently' and then temperature
    current[0] = 1
    current[1] = 1
    current[2] = 1
    current[3] = 1
    current[4] = 1
    current[5] = 1
    current[6] = 1
    current[7] = 1
    current[8] = 1
    current = numberWords(temp[0], current)
    
    # light pixels for words representing 'degrees &' and then wind and forecast
    current[143] = 1
    current[144] = 1
    current[145] = 1
    current[146] = 1
    current[147] = 1
    current[148] = 1
    current[149] = 1
    current[168] = 1
    current = windWords(wind[0], current)
    current = forecastWords(fct[0], current)

    # for min and max upcoming weather conditions
    minTemp = maxTemp = temp[1]
    minHumid = maxHumid = humid[1]
    minWind = maxWind = wind[1]
    minFct = maxFct = fct[1]
    for i in range(1, OBJMAX):
        if int(temp[i]) < int(minTemp):
            minTemp = temp[i]
        if int(temp[i]) > int(maxTemp):
            maxTemp = temp[i]
        if int(humid[i]) < int(minHumid):
            minHumid = humid[i]
        if int(humid[i]) > int(maxHumid):
            maxHumid = humid[i]
        if int(wind[i]) < int(minWind):
            minWind = wind[i]
        if int(wind[i]) > int(maxWind):
            maxWind = wind[i]
        if int(fct[i]) < int(minFct):
            minFct = fct[i]
        if int(fct[i]) > int(maxFct):
            maxFct = fct[i]

    # light pixels for words representing 'upcoming low' and then temperature
    upcomingMin[18] = 1
    upcomingMin[19] = 1
    upcomingMin[20] = 1
    upcomingMin[21] = 1
    upcomingMin[22] = 1
    upcomingMin[23] = 1
    upcomingMin[24] = 1
    upcomingMin[25] = 1
    upcomingMin[14] = 1
    upcomingMin[15] = 1
    upcomingMin[16] = 1
    upcomingMin = numberWords(minTemp, upcomingMin)
    
    # light pixels for words representing 'degrees &' and then wind and forecast
    upcomingMin[143] = 1
    upcomingMin[144] = 1
    upcomingMin[145] = 1
    upcomingMin[146] = 1
    upcomingMin[147] = 1
    upcomingMin[148] = 1
    upcomingMin[149] = 1
    upcomingMin[168] = 1
    upcomingMin = windWords(minWind, upcomingMin)
    upcomingMin = forecastWords(minFct, upcomingMin)

    # light pixels for words representing 'upcoming high' and then temperature
    upcomingMax[18] = 1
    upcomingMax[19] = 1
    upcomingMax[20] = 1
    upcomingMax[21] = 1
    upcomingMax[22] = 1
    upcomingMax[23] = 1
    upcomingMax[24] = 1
    upcomingMax[25] = 1
    upcomingMax[26] = 1
    upcomingMax[27] = 1
    upcomingMax[28] = 1
    upcomingMax[29] = 1
    upcomingMax = numberWords(maxTemp, upcomingMax)
    
    # light pixels for words representing 'degrees &' and then wind and forecast
    upcomingMax[143] = 1
    upcomingMax[144] = 1
    upcomingMax[145] = 1
    upcomingMax[146] = 1
    upcomingMax[147] = 1
    upcomingMax[148] = 1
    upcomingMax[149] = 1
    upcomingMax[168] = 1
    upcomingMax = windWords(maxWind, upcomingMax)
    upcomingMax = forecastWords(maxFct, upcomingMax)

    return current, upcomingMin, upcomingMax

def numberWords(number, array):
    # check number values and light pixels for corresponding number words
    if int(number) < 0:
        # light pixels for words representing 'minus'
        array[30] = 1
        array[31] = 1
        array[32] = 1
        array[33] = 1
        array[34] = 1
        number = number.lstrip('-')
    if len(number) == 3:
        # light pixels for words representing number values in the hundreds
        array[10] = 1
        array[11] = 1
        array[12] = 1
        array[45] = 1
        array[46] = 1
        array[47] = 1
        array[48] = 1
        array[49] = 1
        array[50] = 1
        array[51] = 1
        if int(number[1:]) < 20 and int(number[1:]) >= 11:
            array = teens(number[1:], array)
        else:
            array = tens(number[1], array)
            array = ones(number[2], array)
    elif len(number) == 2:
        if int(number) < 20 and int(number) >= 11:
            array = teens(number, array)
        else:
            array = tens(number[0], array)
            array = ones(number[1], array)
    else:
        if int(number) == 0:
            # light pixels for words representing 'zero'
            array[35] = 1
            array[36] = 1
            array[37] = 1
            array[38] = 1
        else:
            array = ones(number, array)
    return array

def teens(n, a):
    # light pixels for words representing number values in the teens
    if n == '11':
        a[59] = 1
        a[60] = 1
        a[61] = 1
        a[62] = 1
        a[63] = 1
        a[64] = 1
    elif n == '12':
        a[52] = 1
        a[53] = 1
        a[54] = 1
        a[55] = 1
        a[56] = 1
        a[57] = 1
    elif n == '13':
        a[85] = 1
        a[86] = 1
        a[87] = 1
        a[88] = 1
        a[113] = 1
        a[114] = 1
        a[115] = 1
        a[116] = 1
    elif n == '14':
        a[109] = 1
        a[110] = 1
        a[111] = 1
        a[112] = 1
        a[113] = 1
        a[114] = 1
        a[115] = 1
        a[116] = 1
    elif n == '15':
        a[96] = 1
        a[97] = 1
        a[98] = 1
        a[113] = 1
        a[114] = 1
        a[115] = 1
        a[116] = 1
    elif n == '16':
        a[104] = 1
        a[105] = 1
        a[106] = 1
        a[113] = 1
        a[114] = 1
        a[115] = 1
        a[116] = 1
    elif n == '17':
        a[73] = 1
        a[74] = 1
        a[75] = 1
        a[76] = 1
        a[77] = 1
        a[113] = 1
        a[114] = 1
        a[115] = 1
        a[116] = 1
    elif n == '18':
        a[67] = 1
        a[68] = 1
        a[69] = 1
        a[70] = 1
        a[113] = 1
        a[114] = 1
        a[115] = 1
        a[116] = 1
    elif n == '19':
        a[78] = 1
        a[79] = 1
        a[80] = 1
        a[81] = 1
        a[113] = 1
        a[114] = 1
        a[115] = 1
        a[116] = 1
    return a

def tens(n, a):
    # light pixels for words representing number values in the tens
    if n == '1':
        a[150] = 1
        a[151] = 1
        a[152] = 1
    elif n == '2':
        a[39] = 1
        a[40] = 1
        a[41] = 1
        a[42] = 1
        a[43] = 1
        a[44] = 1
    elif n == '3':
        a[85] = 1
        a[86] = 1
        a[87] = 1
        a[88] = 1
        a[89] = 1
        a[90] = 1
    elif n == '4':
        a[99] = 1
        a[100] = 1
        a[101] = 1
        a[102] = 1
        a[103] = 1
    elif n == '5':
        a[94] = 1
        a[95] = 1
        a[96] = 1
        a[97] = 1
        a[98] = 1
    elif n == '6':
        a[104] = 1
        a[105] = 1
        a[106] = 1
        a[107] = 1
        a[108] = 1
    elif n == '7':
        a[71] = 1
        a[72] = 1
        a[73] = 1
        a[74] = 1
        a[75] = 1
        a[76] = 1
        a[77] = 1
    elif n == '8':
        a[65] = 1
        a[66] = 1
        a[67] = 1
        a[68] = 1
        a[69] = 1
        a[70] = 1
    elif n == '9':
        a[78] = 1
        a[79] = 1
        a[80] = 1
        a[81] = 1
        a[82] = 1
        a[83] = 1
    return a

def ones(n, a):
    # light pixels for words representing number values in the ones
    if n == '1':
        a[91] = 1
        a[92] = 1
        a[93] = 1
    elif n == '2':
        a[153] = 1
        a[154] = 1
        a[155] = 1
    elif n == '3':
        a[121] = 1
        a[122] = 1
        a[123] = 1
        a[124] = 1
        a[125] = 1
    elif n == '4':
        a[109] = 1
        a[110] = 1
        a[111] = 1
        a[112] = 1
    elif n == '5':
        a[117] = 1
        a[118] = 1
        a[119] = 1
        a[120] = 1
    elif n == '6':
        a[130] = 1
        a[131] = 1
        a[132] = 1
    elif n == '7':
        a[133] = 1
        a[134] = 1
        a[135] = 1
        a[136] = 1
        a[137] = 1
    elif n == '8':
        a[138] = 1
        a[139] = 1
        a[140] = 1
        a[141] = 1
        a[142] = 1
    elif n == '9':
        a[126] = 1
        a[127] = 1
        a[128] = 1
        a[129] = 1
    return a

def windWords(number, array):
    if int(number) >=5 and int(number) < 20:
        # light pixels for words representing 'breezy'
        array[156] = 1
        array[157] = 1
        array[158] = 1
        array[159] = 1
        array[160] = 1
        array[161] = 1
    elif int(number) >= 20:
        # light pixels for words representing 'windy'
        array[162] = 1
        array[163] = 1
        array[164] = 1
        array[165] = 1
        array[166] = 1
    return array

def forecastWords(number, array):
    if number == '1':
        # light pixels for words representing 'clear'
        array[177] = 1
        array[178] = 1
        array[179] = 1
        array[180] = 1
        array[181] = 1
    elif number == '2':
        # light pixels for words representing 'partly cloudy'
        array[188] = 1
        array[189] = 1
        array[190] = 1
        array[191] = 1
        array[192] = 1
        array[193] = 1
        array[198] = 1
        array[199] = 1
        array[200] = 1
        array[201] = 1
        array[202] = 1
        array[203] = 1
    elif number == '3':
        # light pixels for words representing 'mostly cloudy'
        array[182] = 1
        array[183] = 1
        array[184] = 1
        array[185] = 1
        array[186] = 1
        array[187] = 1
        array[198] = 1
        array[199] = 1
        array[200] = 1
        array[201] = 1
        array[202] = 1
        array[203] = 1
    elif number == '4':
        # light pixels for words representing 'cloudy'
        array[198] = 1
        array[199] = 1
        array[200] = 1
        array[201] = 1
        array[202] = 1
        array[203] = 1
    elif number == '5':
        # light pixels for words representing 'hazy'
        array[173] = 1
        array[174] = 1
        array[175] = 1
        array[176] = 1
    elif number == '6':
        # light pixels for words representing 'foggy'
        array[216] = 1
        array[217] = 1
        array[218] = 1
        array[219] = 1
        array[220] = 1
    elif number == '7':
        # light pixels for words representing 'very hot'
        array[169] = 1
        array[170] = 1
        array[171] = 1
        array[172] = 1
        array[195] = 1
        array[196] = 1
        array[197] = 1
    elif number == '8':
        # light pixels for words representing 'very cold'
        array[169] = 1
        array[170] = 1
        array[171] = 1
        array[172] = 1
        array[204] = 1
        array[205] = 1
        array[206] = 1
        array[207] = 1
    elif number == '9':
        # light pixels for words representing 'blowing snow'
        array[227] = 1
        array[228] = 1
        array[229] = 1
        array[230] = 1
        array[231] = 1
        array[232] = 1
        array[233] = 1
        array[234] = 1
        array[235] = 1
        array[236] = 1
        array[237] = 1
    elif number == '10':
        # light pixels for words representing 'showers likely'
        array[240] = 1
        array[241] = 1
        array[242] = 1
        array[243] = 1
        array[244] = 1
        array[245] = 1
        array[246] = 1
        array[173] = 1
        array[174] = 1
        array[175] = 1
        array[176] = 1
        array[177] = 1
        array[178] = 1
    elif number == '11':
        # light pixels for words representing 'showers'
        array[240] = 1
        array[241] = 1
        array[242] = 1
        array[243] = 1
        array[244] = 1
        array[245] = 1
        array[246] = 1
    elif number == '12':
        # light pixels for words representing 'rain likely'
        array[222] = 1
        array[223] = 1
        array[224] = 1
        array[225] = 1
        array[173] = 1
        array[174] = 1
        array[175] = 1
        array[176] = 1
        array[177] = 1
        array[178] = 1
    elif number == '13':
        # light pixels for words representing 'rain'
        array[222] = 1
        array[223] = 1
        array[224] = 1
        array[225] = 1
    elif number == '14':
        # light pixels for words representing 'thunderstorms likely'
        array[247] = 1
        array[248] = 1
        array[249] = 1
        array[250] = 1
        array[251] = 1
        array[252] = 1
        array[253] = 1
        array[254] = 1
        array[255] = 1
        array[256] = 1
        array[257] = 1
        array[258] = 1
        array[259] = 1
        array[173] = 1
        array[174] = 1
        array[175] = 1
        array[176] = 1
        array[177] = 1
        array[178] = 1
    elif number == '15':
        # light pixels for words representing 'thunderstorms'
        array[247] = 1
        array[248] = 1
        array[249] = 1
        array[250] = 1
        array[251] = 1
        array[252] = 1
        array[253] = 1
        array[254] = 1
        array[255] = 1
        array[256] = 1
        array[257] = 1
        array[258] = 1
        array[259] = 1
    elif number == '16':
        # light pixels for words representing 'flurries'
        array[208] = 1
        array[209] = 1
        array[210] = 1
        array[211] = 1
        array[212] = 1
        array[213] = 1
        array[214] = 1
        array[215] = 1
    elif number == '18':
        # light pixels for words representing 'snow showers likely'
        array[234] = 1
        array[235] = 1
        array[236] = 1
        array[237] = 1
        array[240] = 1
        array[241] = 1
        array[242] = 1
        array[243] = 1
        array[244] = 1
        array[245] = 1
        array[246] = 1
        array[173] = 1
        array[174] = 1
        array[175] = 1
        array[176] = 1
        array[177] = 1
        array[178] = 1
    elif number == '19':
        # light pixels for words representing 'snow showers'
        array[234] = 1
        array[235] = 1
        array[236] = 1
        array[237] = 1
        array[240] = 1
        array[241] = 1
        array[242] = 1
        array[243] = 1
        array[244] = 1
        array[245] = 1
        array[246] = 1
    elif number == '20':
        # light pixels for words representing 'snow likely'
        array[234] = 1
        array[235] = 1
        array[236] = 1
        array[237] = 1
        array[173] = 1
        array[174] = 1
        array[175] = 1
        array[176] = 1
        array[177] = 1
        array[178] = 1
    elif number == '21':
        # light pixels for words representing 'snow'
        array[234] = 1
        array[235] = 1
        array[236] = 1
        array[237] = 1
    elif number == '22':
        # light pixels for words representing 'ice pellets likely'
        array[260] = 1
        array[261] = 1
        array[262] = 1
        array[279] = 1
        array[280] = 1
        array[281] = 1
        array[282] = 1
        array[283] = 1
        array[284] = 1
        array[285] = 1
        array[173] = 1
        array[174] = 1
        array[175] = 1
        array[176] = 1
        array[177] = 1
        array[178] = 1
    elif number == '23':
        # light pixels for words representing 'ice pellets'
        array[260] = 1
        array[261] = 1
        array[262] = 1
        array[279] = 1
        array[280] = 1
        array[281] = 1
        array[282] = 1
        array[283] = 1
        array[284] = 1
        array[285] = 1
    elif number == '24':
        # light pixels for words representing 'blizzard'
        array[265] = 1
        array[266] = 1
        array[267] = 1
        array[268] = 1
        array[269] = 1
        array[270] = 1
        array[271] = 1
        array[272] = 1
    return array

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

    startTime = time.time()             # initialize beginning time between weather updates
    elapsedTime = 0.0                   # initialize elapsed time between weather updates
    boot = True                         # boot bit is used for tracking first call after start up
    success = False                     # success bit is used for tracking the success or failure of api calls
    loopFailCount = 0                   # set intial count of failed api calls
    
    # demonstrate LED strip with all white for all words during Pi startup
    writeLogFile('-----Demonstrate Rainbow Chase-----', 'w')
    rainbow(strip)
    
    # check for internet connection using common url and utilize a red color wipe across the LED matrix if no connection is available
    writeLogFile('\n\n-----Check Internet Connection-----', 'w')
    try:
        response = urlopen('https://www.google.com/').read()
    except:
        writeLogFile('\n\nFailed to connect to internet.', 'a')
        colorWipe(strip, Color(0,255,0))
        raise SystemExit('cannot connect to internet')
    
    # main routine to fetch, parse, and color weather data
    apiVal = readApiBootFile(strip)
    apiUrl = "http://api.wunderground.com/api/" + str(apiVal[0]) + "/hourly/q/" + str(apiVal[1]) + ".json"
    while True:
        # loop through weather functions at designated elapsed time intervals
        elapsedTime = time.time() - startTime
        if (success == True and elapsedTime >= TIME_BETWEEN_CALLS) or (success == False and elapsedTime >= TIME_BETWEEN_FAILED) or (boot == True and elapsedTime >= TIME_WAIT_STARTUP):
            try:
                # attempt to fetch weather data
                writeLogFile('\n\n-----Connecting-----', 'w')
                writeLogFile('\n\n' + str(apiUrl), 'a')
                writeLogFile('\n\nWeather data provided by The Weather Underground, LLC (WUL)', 'a')
                response = urlopen(apiUrl).read().decode('utf8')
            except:
                # handle failed api call
                # utilizes yellow color wipe to signal api call failed at boot
                if boot == True:
                    writeLogFile('\n\nFailed to connect to API at boot.', 'a')
                    colorWipe(strip, Color(255,255,0))
                boot = False
                success = False
                loopFailCount += 1
                startTime = time.time()
                if loopFailCount <= 10:
                    writeLogFile('\n\nFailed to connect to API. Trying again in ' + str(TIME_BETWEEN_FAILED) + ' seconds.', 'a')
                else:
                    # utilizes red color wipe to signal api call failed at boot
                    writeLogFile('\n\nFailed to connect to API after ' + str(loopFailCount) + ' attempts.', 'a')
                    colorWipe(strip, Color(0,255,0))
                    raise SystemExit('cannot connect to API after multiple attempts')
            else:
                # continue after successful api call
                boot = False
                success = True
                startTime = time.time()
                obj = json.loads(response)
                # call function to parse weather data
                writeLogFile('\n\n-----Parsing-----', 'a')
                tempData, humidData, windData, fctData, fctTime = parseWeatherData(strip, obj)
                # call function to assign pixel values to weather data
                writeLogFile('\n\n-----Coloring-----', 'a')
                currentPixels, upcomingMinPixels, upcomingMaxPixels = pixelAssign(tempData, humidData, windData, fctData)
                # display weather data
                writeLogFile('\n\nTemperature Data: ' + str(tempData), 'a')
                writeLogFile('\n\nHumidity Data: ' + str(humidData), 'a')
                writeLogFile('\n\nWind Data: ' + str(windData), 'a')
                writeLogFile('\n\nForecast Data: ' + str(fctData), 'a')
                writeLogFile('\n\nForecast Time: ' + str(fctTime), 'a')
                writeLogFile('\n\nCurrent Weather Pixels: \n' + str(currentPixels), 'a')
                writeLogFile('\n\nUpcoming Min Condition Weather Pixels: \n' + str(upcomingMinPixels), 'a')
                writeLogFile('\n\nUpcoming Max Condition Weather Pixels: \n' + str(upcomingMaxPixels), 'a')
                # call functions to light weather data for each weather word
                elapsedTime = time.time() - startTime
                while elapsedTime < TIME_BETWEEN_CALLS:
                    pixelWipe(strip, currentPixels)
                    writeLogFile('\n\nDisplaying currentPixel Words', 'a')
                    time.sleep(20)
                    pixelWipe(strip, upcomingMinPixels)
                    writeLogFile('\n\nDisplaying upcomingMinPixel Words', 'a')
                    time.sleep(20)
                    pixelWipe(strip, upcomingMaxPixels)
                    writeLogFile('\n\nDisplaying upcomingMaxPixel Words', 'a')
                    time.sleep(20)
                    elapsedTime = time.time() - startTime

main()
