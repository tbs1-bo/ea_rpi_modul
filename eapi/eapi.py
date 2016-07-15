"""Ein Module für die Verwendung des Eingabe-Ausgabe-Moduls für den Raspberry
Pi. Es besteht aus der Hauptklasse EAModul, die für die Ansteuerung vorgesehen
ist."""


# Versuche, die Bibliothek für GPIO-Pins zu laden. Wenn dies scheitert, wird 
# ein Dummy verwendet.
try:
    import RPi.GPIO as GPIO
except ImportError:
    import RPiDummy.GPIO as GPIO
    print("!! Es wird eine Dummy Klasse für GPIO-PINs wird verwendet!!")

class EAModul:
    """Die Klasse EAModul hilft bei der Ansteuerung eines Eingabe-Ausgabe-Moduls
    für den Raspberry Pi. Es besteht aus drei LED und zwei Tastern."""

    LED_ROT = 0
    LED_GELB = 1
    LED_GRUEN = 2

    def __init__(self, pin_taster0=29, pin_taster1=31, pin_led0=33, pin_led1=35, pin_led2=37):
        """
        Die PINs des Moduls werden konfiguriert.

        Pins der LED werden als Ausgänge, und Pins der Taster als Eingänge
        konfiguriert. Wenn keine PINS angegeben werden, werden die PINs
        oberhalb des GND Pins links unten verwendet.
        """
        GPIO.setmode(GPIO.BOARD)

        self.__taster = [pin_taster0, pin_taster1]
        GPIO.setup(self.__taster, GPIO.IN)

        self.__leds = [pin_led0, pin_led1, pin_led2]
        GPIO.setup(self.__leds, GPIO.OUT)


    def taster_gedrueckt(self, num=0):
        """
        Liest den Wert des Tasters mit der gegebenen Nummer aus und gibt den
        Wert zurück.
        """
        if 0 <= num < len(self.__taster):
            return GPIO.input(self.__taster[num])
        else:
            raise Exception(
                "Falsche Tasternummer. Muss zwischen 0 und {ln} liegen.".format(
                    ln=len(self.__taster)-1))


    def schalte_led(self, num=0, an_aus=True):
        """
        Schalte die LED mit der gegebenen Nummer ein (True) oder aus (False).
        """
        if 0 <= num < len(self.__leds):
            return GPIO.output(self.__leds[num], an_aus)
        else:
            raise Exception(
                "Falsche LED-Nummer. Muss zwischen 0 und {ln} liegen.".format(
                    ln=len(self.__leds)-1))

    def taster_event_registrieren(self, taster_nr, methode):
        """Registriere eine Methode, die bei Betätigung ausgeführt wird.

        Die übergebene Methode muss ein Argument haben und wird mit der
        Pin-Nur des Tasters aufgerufen, sobald der Taster gedrückt
        oder losgelassen wird."""
        if taster_nr < 0 or taster_nr >= len(self.__taster):
            raise Exception("Falsche Taster Nummer." + taster_nr)

        GPIO.add_event_detect(self.__taster[taster_nr], GPIO.BOTH)
        GPIO.add_event_callback(self.__taster[taster_nr], methode)


    def cleanup(self):
        """Setzt alle Pins des Pi wieder in den Ausgangszustand."""
        GPIO.cleanup()

