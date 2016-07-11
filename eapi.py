import RPi.GPIO as GPIO

class EAModul:
    def __init__(self, pin_taster1, pin_taster2, pin_led1, pin_led2, pin_led3):
        GPIO.cleanup()
        GPIO.setmode(GPIO.BOARD)

        self.__taster = [pin_taster1, pin_taster2]
        GPIO.setup(self.__taster, GPIO.IN)

        self.__leds = [pin_led1, pin_led2, pin_led3]
        GPIO.setup(self.__leds, GPIO.OUT)
        

    def lies_taster(self, nr=0):
        if 0 <= nr < len(self.__taster):
            return GPIO.input(self.__taster[nr])
        else:
            raise Exception("Falsche Tasternummer. Muss 1 oder 2 sein.")


    def schalte_led(self, nr=0, an_aus=True):
        if 0 <= nr < len(self.__leds):
            return GPIO.output(self.__leds[nr], an_aus)
        else:
            raise Exception("Falsche LED-Nummer. Muss 1 oder 2 sein.")        


    def cleanup(self):
        GPIO.cleanup()


if __name__ == "__main__":
    ea = EAModul(1,2,3,4)
    ea.schalte_led(1, True)
    ea.schalte_led(1, False)
    ea.cleanup()

