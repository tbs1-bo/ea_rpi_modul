from eapi.eapi import EAModul
import time
import RPi.GPIO as GPIO

if __name__ == "__main__":
    # 6 PINs unten links auf dem Pi verwenden. 1 PIN oben links für 3,3V.
    # 2 Taster, 3 LEDs und 1 GND
    #ea_modul = EAModul(29, 31, 33, 35, 37)
    ea_modul = EAModul()

    def taster0_gedrueckt(pin):
        global ea_modul
        ea_modul.schalte_led(EAModul.LED_GELB, ea_modul.taster_gedrueckt(0))

    ea_modul.taster_event_registrieren(0, taster0_gedrueckt)

    try:
        while not ea_modul.taster_gedrueckt(1):
            ea_modul.schalte_led(EAModul.LED_ROT, True)
            time.sleep(0.2)
            ea_modul.schalte_led(EAModul.LED_ROT, False)
            time.sleep(0.2)

            ea_modul.schalte_led(EAModul.LED_GRUEN, True)
            time.sleep(0.5)
            ea_modul.schalte_led(EAModul.LED_GRUEN, False)
            time.sleep(0.2)

    except KeyboardInterrupt:
        ea_modul.cleanup()
    finally:
        ea_modul.cleanup()
