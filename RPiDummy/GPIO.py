import random
import logging

# Konstanten
BOARD = 1
IN = 2
OUT = 3
PUD_DOWN = 4

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

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
    log.info("Setup pin {p} modus {m}".format(p=pin, m=in_out))

def output(pin, an_aus):
    log.info("Output {a} an pin {p}".format(a=an_aus, p=pin))

def cleanup():
    log.info("cleanup")
