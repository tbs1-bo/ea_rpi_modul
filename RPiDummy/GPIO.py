import random
import logging

# Konstanten
BOARD = 1
IN = 2
OUT = 3
PUD_DOWN = 4

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

PINS = {}

def __alle_pins_ausgeben():
    s = "PIN-BELEGUNGEN: "
    for p in PINS:        
        s += "{pin}:{on} ".format(pin=p, on=PINS[p])
    log.debug(s)

def input(pin):
    """Dummy Methode, die zufällig True oder False zurückgibt."""
    log.info("Input für pin " + str(pin))
    if random.randint(0, 1) == 0:
        return True
    else:
        return False
        
def setmode(board):    
    """Macht nichts."""
    log.info("Setze boardmode auf " + str(board))

def setup(pin, in_out):
    """Macht nichts."""    
    global PINS
    log.info("Setup pin {p} modus {m}".format(p=pin, m=in_out))
    if type(pin) is list:
        for p in pin:
            setup(p, in_out)
        return

    PINS[pin] = False

def output(pin, an_aus):
    global PINS
    log.info("Output {a} an pin {p}".format(a=an_aus, p=pin))
    PINS[pin] = an_aus
    __alle_pins_ausgeben()

def cleanup():
    log.info("cleanup")

