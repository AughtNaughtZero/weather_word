# weather_word

This project utilizes a 22 x 13 matrix of RGB LEDs to visualize weather forecast data pulled from an API.

The Weather Word program is designed to fetch weather forecast data from an API in regular intervals, parse the data 
into temperature, wind speed, and weather condition arrays, and then light specific sets of LEDs that represent words 
in the 22 x 13 LED matrix. The program will also generate the file log.txt which is used for general 
troubleshooting and data review. The file is re-written at each API call.
 
The apiboot.txt and weather_word.py files are intended to reside at /home/pi/weather_word directory and to be launched at 
startup by editing crontab with the instruction @reboot sudo python3 /home/pi/weather_word/weather_word.py.
 
A tutorial for the complete project can be found at www.instructables.com/id/LED-Weather-Words-Forecast. The basic
hardware and software setup can be found at https://learn.adafruit.com/neopixels-on-raspberry-pi. The NeoPixel library
for the Raspberry Pi (rpi_ws281x library) can be found at https://github.com/jgarff. The weather data and API are provided
by Weather Underground, LLC (WUL). An API key can be obtained at www.wunderground.com/weather/api.

CAUTION - This project contains 286 LEDs that together could pull as much as 17 amps at full brightness setting (60mA per
pixel when set at 255,255,255 multiplied by 286 pixels equals 17.16 amps total). This current draw exceeds the capability of
the hardware as published (breadboard, connecting wires, 4 amp power supply). Setting the brightness beyond the values 
already set in this program could lead to hardware failure or injury. Additionally, depending on the type and quality of
hardware used in duplicating this project, it may be necessary to lower brightness settings further to reduce current draw. 
