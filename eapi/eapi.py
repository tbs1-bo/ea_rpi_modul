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

    def __init__(self, pin_taster0, pin_taster1, pin_led0, pin_led1, pin_led2):
        """
        Die PINs des Moduls werden konfiguriert. Pins der LED werden als
        Ausgänge, und Pins der Taster als Eingänge konfiguriert.
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


    def cleanup(self):
        """Setzt alle Pins des Pi wieder in den Ausgangszustand."""
        GPIO.cleanup()

