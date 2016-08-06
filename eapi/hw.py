"""Ein Modul für die Verwendung des Eingabe-Ausgabe-Moduls für den Raspberry
Pi.

Es besteht aus der Hauptklasse EAModul, die für die Ansteuerung vorgesehen
ist. Hierfür existieren verschiedene Demos, die von der Kommandozeile aus
aufgerufen werden können:

  $ python3 -m eapi.hw

"""


# Versuche, die Bibliothek für GPIO-Pins zu laden. Wenn dies scheitert, wird 
# ein Dummy verwendet.
try:
    import RPi.GPIO as GPIO
except ImportError:
    import eapi.GPIODummy as GPIO


class EAModul:
    """Die Klasse EAModul hilft bei der Ansteuerung eines Eingabe-Ausgabe-Moduls
    für den Raspberry Pi. Es besteht aus drei LED und zwei Tastern."""

    LED_ROT = 0
    LED_GELB = 1
    LED_GRUEN = 2

    def __init__(self, pin_taster0=29, pin_taster1=31, pin_led_rot=33, pin_led_gelb=35, pin_led_gruen=37):
        """
        Die PINs des Moduls werden konfiguriert.

        Pins der LED werden als Ausgänge, und Pins der Taster als Eingänge
        konfiguriert. Wenn keine PINS angegeben werden, werden die PINs
        oberhalb des GND Pins links unten verwendet.

        >>> from eapi.hw import EAModul

        >>> ea = EAModul()
        >>> ea.cleanup()
        """
        GPIO.setmode(GPIO.BOARD)

        self.__taster = [pin_taster0, pin_taster1]
        GPIO.setup(self.__taster, GPIO.IN)

        self.__leds = [pin_led_rot, pin_led_gelb, pin_led_gruen]
        GPIO.setup(self.__leds, GPIO.OUT)

        # Für jede LED wird ein PWM bereitgestellt, ueber den die LED 
        # gedimmt werden kann
        self.__pwms = [
            GPIO.PWM(pin_led_rot, 50),
            GPIO.PWM(pin_led_gelb, 50),
            GPIO.PWM(pin_led_gruen, 50)
            ]
        for pwm in self.__pwms:
            pwm.start(0)

    def taster_gedrueckt(self, num=0):
        """
        Liest den Wert des Tasters mit der gegebenen Nummer aus und gibt den
        Wert zurück. Eine einfache Verwendung könnte wie folgt aussehen:

        >>> from eapi.hw import EAModul
        >>> import time

        >>> ea_modul = EAModul()
        >>> while not ea_modul.taster_gedrueckt(1):
        ...   ea_modul.schalte_led(EAModul.LED_ROT, 1)
        ...   time.sleep(0.2)
        ...   ea_modul.schalte_led(EAModul.LED_ROT, 0)
        >>> ea_modul.cleanup()
        """
        if 0 <= num < len(self.__taster):
            if GPIO.input(self.__taster[num]):
                return True
            else:
                return False
        else:
            raise Exception(
                "Falsche Tasternummer. Muss zwischen 0 und {ln} liegen.".format(
                    ln=len(self.__taster)-1))

    def schalte_led(self, led_farbe, helligkeit):
        """Schalte die LED mit der gegebenen Nummer ein (1) oder aus (0).

        Der Wert für led_farbe ist LED_ROT, LED_GELB oder LED_GRUEN.

        Wenn für helligkeit eine Kommazahl zwischen 0 und 1 angegeben
        wird, lässt sich die LED dimmen: ein Wert von 0.5 lässt die
        LED nur mit halber Kraft leuchten.

        Eine einfache Verwendung könnte wie folgt aussehen:

        >>> from eapi.hw import EAModul

        >>> ea_modul = EAModul()
        >>> ea_modul.schalte_led(EAModul.LED_ROT, 1)
        >>> ea_modul.schalte_led(EAModul.LED_GELB, 0)
        >>> ea_modul.schalte_led(EAModul.LED_GRUEN, 0.5)
        >>> ea_modul.cleanup()
        """

        if 0 <= led_farbe < len(self.__leds):
            if 0 <= helligkeit <= 1:
                # LED dimmen
                pwm = self.__pwms[led_farbe]
                pwm.ChangeDutyCycle(helligkeit*100)

            else:
                raise Exception("Wert für Helligkeit muss zwischen 0 und 1 liegen.")
        else:
            raise Exception("Falsche LED-Farbe.")

    def taster_event_registrieren(self, taster_nr, methode):
        """Registriere eine Methode, die bei Betätigung ausgeführt wird.

        Die übergebene Methode muss ein Argument haben und wird mit der
        Pin-Nur des Tasters aufgerufen, sobald der Taster gedrückt oder
        losgelassen wird. Eine einfache Verwendung könnte wie folgt aussehen:

        >>> from eapi.hw import EAModul

        >>> def taster0_gedrueckt(pin):
        ...  print("Taster 0 wurde gedrückt.")

        >>> ea_modul = EAModul()
        >>> ea_modul.taster_event_registrieren(0, taster0_gedrueckt)
        >>> ea_modul.cleanup()
        """
        if taster_nr < 0 or taster_nr >= len(self.__taster):
            raise Exception("Falsche Taster Nummer." + taster_nr)

        GPIO.add_event_detect(self.__taster[taster_nr], GPIO.BOTH)
        GPIO.add_event_callback(self.__taster[taster_nr], methode)

    def cleanup(self):
        """Setzt alle Pins des Pi wieder in den Ausgangszustand.

        >>> from eapi.hw import EAModul
        >>> ea = EAModul()
        >>> ea.cleanup()
        """
        GPIO.cleanup()


if __name__ == "__main__":
    import time

    __command = input("Befehl angeben: demo_led_taster demo_dimmen: ")
    if __command == "demo_dimmen":        
        input("Alle LEDs werden 0.0 auf 1.0 gedimmt und dann von 1.0 auf 0.0 (Enter)")
        __ea_modul = EAModul()
        for i in range(100):
            __ea_modul.schalte_led(EAModul.LED_ROT, i/100)
            __ea_modul.schalte_led(EAModul.LED_GELB, i/100)
            __ea_modul.schalte_led(EAModul.LED_GRUEN, i/100)
            time.sleep(0.05)
        for i in range(100):
            __ea_modul.schalte_led(EAModul.LED_ROT, 1-i/100)
            __ea_modul.schalte_led(EAModul.LED_GELB, 1-i/100)
            __ea_modul.schalte_led(EAModul.LED_GRUEN, 1-i/100)
            time.sleep(0.05)

        __ea_modul.cleanup()

    elif __command == "demo_led_taster":
        input(
            """
            Die rote und grüne LED blinken abwechselnd. Gleichzeitig kann über den einen 
            Taster die gelbe LED an- und ausgeschaltet werden. Der andere Taster beendet
            das Programm, wenn er länger gedrückt wird.
            (Enter)
            """)

        __ea_modul = EAModul()

        def __taster0_gedrueckt(pin):
            global __ea_modul
            __ea_modul.schalte_led(EAModul.LED_GELB, __ea_modul.taster_gedrueckt(0))

        __ea_modul.taster_event_registrieren(0, __taster0_gedrueckt)

        try:
            while not __ea_modul.taster_gedrueckt(1):
                __ea_modul.schalte_led(EAModul.LED_ROT, 1)
                time.sleep(0.2)
                __ea_modul.schalte_led(EAModul.LED_ROT, 0)
                time.sleep(0.2)

                __ea_modul.schalte_led(EAModul.LED_GRUEN, 1)
                time.sleep(0.5)
                __ea_modul.schalte_led(EAModul.LED_GRUEN, 0)
                time.sleep(0.2)

        except KeyboardInterrupt:
            __ea_modul.cleanup()
        finally:
            __ea_modul.cleanup()
