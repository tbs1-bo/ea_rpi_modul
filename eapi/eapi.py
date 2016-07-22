"""Ein Modul für die Verwendung des Eingabe-Ausgabe-Moduls für den Raspberry
Pi. Es besteht aus der Hauptklasse EAModul, die für die Ansteuerung vorgesehen
ist.

Es existieren verschiedene Demos, die von der Kommandozeile aus aufgerufen
werden können:

  $ python3 -m eapi.api

"""


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

        # Für jede LED wird ein PWM bereitgestellt, ueber den die LED 
        # gedimmt werden kann
        self.__pwms = [
            GPIO.PWM(pin_led0, 100),
            GPIO.PWM(pin_led1, 100),
            GPIO.PWM(pin_led2, 100)
            ]




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
        """Schalte die LED mit der gegebenen Nummer ein (True, 1) oder aus (False, 0).

        Wenn für an_aus eine Kommazahl zwischen 0 und 1 angegeben
        wird, lässt sich die LED dimmen: ein Wert von 0.5 lässt die
        LED nur mit halber Kraft leuchten."""

        if 0 <= num < len(self.__leds):
            if isinstance(an_aus, int) or isinstance(an_aus, bool):
                # LED ein oder ausschalten
                self.__pwms[num].stop()
                GPIO.output(self.__leds[num], an_aus)

            elif isinstance(an_aus, float) and 0 <= an_aus <= 1:
                # LED dimmen
                pwm = self.__pwms[num]
                pwm.start(0)
                pwm.ChangeDutyCycle(an_aus*100)

            else:
                raise Exception(
                    "Wert für an_aus muss zwischen 0 und 1 liegen oder bool sein.")
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


if __name__ == "__main__":
    import time

    command = input("Befehl angeben: demo_led_taster demo_dimmen: ")
    if command == "demo_dimmen":        
        input("Alle LEDs werden 0.0 auf 1.0 gedimmt und dann von 1.0 auf 0.0 (Enter)")
        ea_modul = EAModul()
        for i in range(100):
            ea_modul.schalte_led(EAModul.LED_ROT, i/100)
            ea_modul.schalte_led(EAModul.LED_GELB, i/100)
            ea_modul.schalte_led(EAModul.LED_GRUEN, i/100)
            time.sleep(0.05)
        for i in range(100):
            ea_modul.schalte_led(EAModul.LED_ROT, 1-i/100)
            ea_modul.schalte_led(EAModul.LED_GELB, 1-i/100)
            ea_modul.schalte_led(EAModul.LED_GRUEN, 1-i/100)
            time.sleep(0.05)

        ea_modul.cleanup()

    elif command == "demo_led_taster":
        input(
            """
            Die rote und grüne LED blinken abwechselnd. Gleichzeitig kann über den einen 
            Taster die gelbe LED an- und ausgeschaltet werden. Der andere Taster beendet
            das Programm, wenn er länger gedrückt wird.
            (Enter)
            """)

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
