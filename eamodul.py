#!/usr/bin/env python3
"""This script can be installed on you pi. Together with the EA-Modul
it provides the possibilty to turn off the pi with the press of a
button (for 5 seconds). Further the green LED is pulsing when the pi
is started. You can stop this script by pressing the other button (for
2 seconds).

INSTALLATION:

1. Copy the file to /home/pi/bin/eamodul.py

2. Install the script in your crontab such that it will be executed on
   startup:

   $ crontab -e

   Insert the following line
  
   @reboot /home/pi/bin/eamodul.py

3. Have fun :)


If the EAModul should be used otherwise, the script can be terminated
by pressing the other button.

"""

import gpiozero
import os
import time

# pins are considered in BCM
green_pin = 26
taster0_pin = 5
taster1_pin = 6

led = gpiozero.PWMLED(green_pin)

def btn0_held():
    print("Button0 held")
    os.system("sudo shutdown -h now")

def btn1_held():
    print("Button1 held")
    led.close()

    # fetch process id and kill myself    
    # simple exit does not work due to several threads
    pid = os.getpid()
    os.system("kill " + str(pid))

def main():    
    print("Starting")

    btn0 = gpiozero.Button(taster0_pin, pull_up=False, hold_time=5)
    btn0.when_held = btn0_held

    btn1 = gpiozero.Button(taster1_pin, pull_up=False, hold_time=2)
    btn1.when_held = btn1_held

    led.pulse()

    while True:
        time.sleep(100)


if __name__ == "__main__":
    main()
