import random
import logging

# Konstanten
BOARD = 1
IN = 2
OUT = 3
PUD_DOWN = 4
BOTH = 5

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

__PINS = {}

def __alle_pins_ausgeben():
    s = "PIN-BELEGUNGEN: "
    for p in __PINS:        
        s += "{pin}:{on} ".format(pin=p, on=__PINS[p])
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
    global __PINS
    log.info("Setup pin {p} modus {m}".format(p=pin, m=in_out))
    if type(pin) is list:
        for p in pin:
            setup(p, in_out)
        return

    __PINS[pin] = False

def output(pin, an_aus):
    global __PINS
    log.info("Output {a} an pin {p}".format(a=an_aus, p=pin))
    __PINS[pin] = an_aus
    __alle_pins_ausgeben()

def cleanup():
    log.info("cleanup")

def add_event_detect(pin, flanke):
    log.info("Event registrieren für Pin " + str(pin))

def add_event_callback(pin, methode):
    log.info("Registriere Callback Methode {m} für Pin {p}".format(m=methode, p=pin))

